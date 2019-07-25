import sys
from threading import Thread

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from FullSend.authhelper import get_signin_url, get_token_from_code, get_access_token
from mail.outlookservice import get_me, get_my_messages, generate_email, send_message
from mail.formhandler import MailForm, QuickForm

# Create your views here.


def home(request):
  redirect_uri = request.build_absolute_uri(reverse('mail:gettoken'))
  sign_in_url = get_signin_url(redirect_uri)
  context = {'signin_url': sign_in_url}
  return render(request, 'mail/home.html', context)

@csrf_exempt
def bounce(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    if 'key' not in request.headers or request.headers['key'] != 'abc':
        return HttpResponseForbidden()
    return HttpResponse('This part is in the works.')
