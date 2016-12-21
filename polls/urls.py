from django.conf.urls import url
from .views import detail

urlpatterns = [
    url(r'^(?P<poll_id>\w+)$', detail),
]
