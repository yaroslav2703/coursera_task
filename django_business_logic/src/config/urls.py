from django.urls import include
from django.conf.urls import url

urlpatterns = [
    url(r'^routing/', include('routing.urls')),
    url(r'^template/', include('template.urls')),
]
