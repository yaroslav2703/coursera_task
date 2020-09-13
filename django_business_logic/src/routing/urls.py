from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    url(r'^simple_route/', csrf_exempt(views.simple_route)),
    url(r'^slug_route/((?P<slug>[a-z0-9_-]{1,16})/){1,}', csrf_exempt(views.slug_route)),
    url(r'^sum_route/(?P<first>[0-9-]{1,})/(?P<second>[0-9-]{1,})/', csrf_exempt(views.sum_route)),
    url(r'^sum_get_method/$', csrf_exempt(views.sum_get_method)),
    url(r'^sum_post_method/', csrf_exempt(views.sum_post_method))
]
