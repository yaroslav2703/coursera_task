from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import echo, filters, extend

urlpatterns = [
    url(r'^echo/$', csrf_exempt(echo)),
    url(r'^filters/$', filters),
    url(r'^extend/$', extend),
]
