import time
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from FullSend.authhelper import get_signin_url, get_token_from_code, get_access_token
from mail.outlookservice import get_me, get_my_messages, generate_email, send_message
from mail.formhandler import MailForm

# Create your views here.
def home(request):
  redirect_uri = request.build_absolute_uri(reverse('mail:gettoken'))
  sign_in_url = get_signin_url(redirect_uri)
  context = {'signin_url': sign_in_url}
  return render(request, 'mail/home.html', context)

def gettoken(request):
  auth_code = request.GET['code']
  redirect_uri = request.build_absolute_uri(reverse('mail:gettoken'))
  token = get_token_from_code(auth_code, redirect_uri)
  access_token = token['access_token']
  user = get_me(access_token)
  refresh_token = token['refresh_token']
  expires_in = token['expires_in']

  # expires_in is in seconds
  # Get current timestamp (seconds since Unix Epoch) and
  # add expires_in to get expiration time
  # Subtract 5 minutes to allow for clock differences
  expiration = int(time.time()) + expires_in - 300

  # Save the token in the session
  request.session['access_token'] = access_token
  request.session['refresh_token'] = refresh_token
  request.session['token_expires'] = expiration
  return HttpResponseRedirect(reverse('mail:getmail'))

def getmail(request):
  access_token = get_access_token(request, request.build_absolute_uri(reverse('mail:gettoken')))
  # If there is no token in the session, redirect to home
  if not access_token:
    return HttpResponseRedirect(reverse('mail:home'))
  else:
    messages = get_my_messages(access_token)
    context = { 'messages': messages['value'] }
    return render(request, 'mail/getmail.html', context)

def sendmail(request):
    access_token = get_access_token(request, request.build_absolute_uri(reverse('mail:gettoken')))
    # If there is no token in the session, redirect to home
    if not access_token:
      return HttpResponseRedirect(reverse('mail:home'))
    else:
      if request.method == 'POST':
        form = MailForm(request.POST, request.FILES)
        if form.is_valid():
            emails = generate_email(form.clean())
            messages = send_message(access_token, emails)
            return HttpResponseRedirect('/')
      else:
        form = MailForm()
      return render(request, 'mail/sendmail.html', {'form': form})
        # Do stuff with the form post
        # messages = test_send_message(access_token)
        # return HttpResponse('Message')
