import sys
import json
import time
import os
import requests
from sentry_sdk import add_breadcrumb, capture_message
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseServerError
from django.urls import reverse

from FullSend.authhelper import get_signin_url, get_token_from_code, get_access_token
from FullSend.authhelper import api_key_required, post_required, get_token_from_refresh_token
from mail.outlookservice import get_me, get_my_messages, generate_email, send_message, make_api_call
from mail.formhandler import MailForm, QuickForm
from api.googleservice import get_email_subject, has_valid_template_type
from api.models import ServerAuthentication
from api.format_service import format_email

# Create your views here.


def home(request):
  redirect_uri = request.build_absolute_uri(reverse('mail:gettoken'))
  sign_in_url = get_signin_url(redirect_uri)
  context = {'signin_url': sign_in_url}
  return render(request, 'mail/home.html', context)

def bounce(request):
    return HttpResponse('This part is in the works.')

def authorize(request):
    redirect_uri = request.build_absolute_uri(reverse('api:storetoken'))
    sign_in_url = get_signin_url(redirect_uri)
    return HttpResponse(f'Please visit here to sign in: <a href={sign_in_url}>{sign_in_url}</a>')

def showtoken(request):
    auth = ServerAuthentication.get_authentication()
    if auth is None or auth.is_out_of_date():
        return HttpResponse('Did not find any authentication.', status=500)
    else:
        return HttpResponse('Found authentication.', status=200)

def storetoken(request):
    # There should only ever be onen ServerAuthentication, so update the most recent one
    auth = ServerAuthentication.get_authentication()

    auth_code = request.GET['code']
    redirect_uri = request.build_absolute_uri(reverse('api:storetoken'))
    token = get_token_from_code(auth_code, redirect_uri)
    access_token = token['access_token']
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
            token_expires=expiration,
            redirect_uri=redirect_uri)
    else:
        auth.access_token = access_token
        auth.refresh_token = refresh_token
        auth.token_expires = expiration
        auth.redirect_uri = redirect_uri

    auth.save()

    return HttpResponseRedirect(reverse('api:showtoken'))

@api_key_required
@post_required
def formsubmit(request):
    access_token = ServerAuthentication.get_authentication().access_token

    if request.body is None:
        return HttpResponseBadRequest('Body is empty')

    settings = json.loads(request.body)
    if not has_valid_template_type(settings['type']):
        return HttpResponseBadRequest('Type was invalid')

    email = {
        'message': {
            'subject': get_email_subject(settings['type']),
            'body': {
                'contentType': 'HTML',
                'content': format_email(settings['type'], settings)
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

    add_breadcrumb(
        category='email',
        message=email,
        level='info',
    )

    # Copy from outlookservice
    graph_endpoint = 'https://graph.microsoft.com/v1.0{0}'
    post_messages_url = graph_endpoint.format('/me/sendMail')
    res = make_api_call('POST', post_messages_url,
                        access_token, payload=email)
    if res.status_code != requests.codes.accepted:
        return HttpResponseServerError(f'Server token probably expired: {res.text}')

    capture_message('Email sent successfully')

    return HttpResponse('This part is in the works.')
