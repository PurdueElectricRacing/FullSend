from django.db import models
import sys
import time

# Create your models here.
class ServerAuthentication(models.Model):
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_expires = models.IntegerField()
    redirect_uri = models.URLField()

    @staticmethod
    def get_authentication():
        auth = ServerAuthentication.objects.all().first()
        if auth is not None:
            print('Received auth: {} until {}'.format(auth.access_token[:10], str(auth.token_expires)))
        else:
            print('No auth available')
        sys.stdout.flush()
        return auth

    def is_out_of_date(auth):
        return int(time.time()) > auth.token_expires
