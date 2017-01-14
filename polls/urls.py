from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^authorize$', views.authorize),
    url(r'^me$', views.me),
    url(r'^my/polls$', views.my_polls),
    url(r'^polls$', views.create_poll),
    url(r'^polls/(?P<poll_id>\w+)$', views.get_detail),
    url(r'^polls/(?P<poll_id>\w+)/vote$', views.make_poll),
]
