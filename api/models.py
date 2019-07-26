from django.db import models
import sys

# Create your models here.
class ServerAuthentication(models.Model):
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_expires = models.IntegerField()

    @staticmethod
    def get_authentication():
        auth = ServerAuthentication.objects.all().first()
        if auth is not None:
            print('Received auth: {} until {}'.format(auth.access_token[:10], str(auth.token_expires)))
        else:
            print('No auth available')
        sys.stdout.flush()
        return auth
