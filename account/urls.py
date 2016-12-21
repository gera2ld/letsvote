from django.conf.urls import url
from .views import callback, logout_view

urlpatterns = [
    url(r'^callback$', callback),
    url(r'^logout$', logout_view),
]
