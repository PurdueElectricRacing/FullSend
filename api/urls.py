from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from api import views

app_name = 'api'
urlpatterns = [
  # List all available API commands
  url(r'^$', views.home, name='home'),

  # API endpoints
  url(r'^bounce/$', csrf_exempt(views.bounce), name='bounce'),
  url(r'^authorize/$', csrf_exempt(views.authorize), name='authorize'),
  url(r'^storetoken/$', csrf_exempt(views.storetoken), name='storetoken'),
  url(r'^showtoken/$', csrf_exempt(views.showtoken), name='showtoken'),
  url(r'^formsubmit/$', csrf_exempt(views.formsubmit), name='formsubmit')
]
