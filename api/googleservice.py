import time
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from sentry_sdk import capture_message, add_breadcrumb, capture_exception

from FullSend.authhelper import get_token_from_refresh_token
from api.models import ServerAuthentication

def refreshtoken():
    auth = ServerAuthentication.get_authentication()
    now = int(time.time())
    if auth is not None and now < auth.token_expires:
        try:
            redirect_uri = auth.redirect_uri
            refresh_token = auth.refresh_token
            new_tokens = get_token_from_refresh_token(refresh_token, redirect_uri)

            expiration = int(time.time()) + new_tokens['expires_in'] - 300
            auth.access_token = new_tokens['access_token']
            auth.refresh_token = new_tokens['refresh_token']
            auth.token_expires = expiration
            auth.redirect_uri = redirect_uri
            
            add_breadcrumb(message='access_token: {}\nrefresh_token: {}\ntoken_expires: {}\nredirect_uri" {}'.format(
                auth.access_token[:10], auth.refresh_token[:10], str(auth.token_expires), auth.redirect_uri))

            auth.save()
            capture_message('Updated access token {} for time {}'.format(
            auth.access_token[:10], str(auth.token_expires)))
        except Exception as e:
            capture_exception(e)


def p():
    capture_message('ping', level='info')

def event_listener(event):
    if event.exception:
        capture_message('Scheduler event to refresh token failed!', 'error')

def get_email_template(template_name):
    return template_name

scheduler = BackgroundScheduler()
# Add a degree of randomness (46-54) so it's not executing at a precise time
scheduler.add_job(refreshtoken, 'cron', minute='50', jitter=240)
scheduler.add_job(p, 'cron', minute='*', replace_existing=True, max_instances=1)
scheduler.add_listener(
    event_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
scheduler.start()
