from django.conf.urls import url
from mail import views

app_name = 'mail'
urlpatterns = [
  # The home view ('/mail/')
  url(r'^$', views.home, name='home'),
  # Explicit home ('/mail/home/')
  url(r'^home/$', views.home, name='home'),
  # Redirect to get token ('/mail/gettoken/')
  url(r'^gettoken/$', views.gettoken, name='gettoken'),
  # Mail view ('/mail/getmail/')
  url(r'^getmail/$', views.getmail, name='getmail'),
]
