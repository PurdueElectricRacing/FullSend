import sys
import json
import time
import os
import requests
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseBadRequest
from django.urls import reverse

from FullSend.authhelper import get_signin_url, get_token_from_code, get_access_token
from FullSend.authhelper import api_key_required, post_required
from mail.outlookservice import get_me, get_my_messages, generate_email, send_message, make_api_call
from mail.formhandler import MailForm, QuickForm
from api.googleservice import get_email_template
from api.models import ServerAuthentication

# Create your views here.


def home(request):
  redirect_uri = request.build_absolute_uri(reverse('mail:gettoken'))
  sign_in_url = get_signin_url(redirect_uri)
  context = {'signin_url': sign_in_url}
  return render(request, 'mail/home.html', context)

def bounce(request):
    return HttpResponse('This part is in the works.')

def authorize(request):
    redirect_uri = request.build_absolute_uri(reverse('api:showtoken'))
    sign_in_url = get_signin_url(redirect_uri)
    return HttpResponse(f'Please visit here to sign in: <a href={sign_in_url}>{sign_in_url}</a>')

def showtoken(request):
    # There should only ever be onen ServerAuthentication, so update the most recent one
    auth = ServerAuthentication.get_authentication()

    auth_code = request.GET['code']
    redirect_uri = request.build_absolute_uri(reverse('api:showtoken'))
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

    if auth is None:
        auth = ServerAuthentication(
            access_token=access_token,
            refresh_token=refresh_token,
            token_expires=expiration)
    else:
        auth.access_token = access_token
        auth.refresh_token = refresh_token
        auth.token_expires = expiration

    auth.save()

    return HttpResponse('Success.')

@api_key_required
@post_required
def formsubmit(request):
    access_token = ServerAuthentication.get_authentication().access_token

    if request.body is None:
        return HttpResponseBadRequest('Body is empty')
    settings = json.loads(request.body)
    email = {
        'message': {
            'subject': 'Test email',
            'body': {
                'contentType': 'HTML',
                'content': get_email_template('Lol what\'s up my dude this is from Django')
            },
            'toRecipients': [
                {
                    'emailAddress': {
                        'address': settings['email']
                    }
                }
            ]
        }
    }

    # Copy from outlookservice
    graph_endpoint = 'https://graph.microsoft.com/v1.0{0}'
    post_messages_url = graph_endpoint.format('/me/sendMail')
    res = make_api_call('POST', post_messages_url,
                        access_token, payload=email)
    if res.status_code != requests.codes.accepted:
        return "{0}: {1}".format(res.status_code, res.text)

    return HttpResponse('This part is in the works.')
