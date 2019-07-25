from django.conf.urls import url
from api import views

app_name = 'api'
urlpatterns = [
  # The home view ('/api/')
  url(r'^$', views.home, name='home'),
  # Explicit home ('/api/bounce/')
  url(r'^bounce/$', views.bounce, name='bounce')
]
