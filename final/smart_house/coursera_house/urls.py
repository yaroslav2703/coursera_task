
from django.conf.urls import url
from coursera_house.core.views import ControllerView

urlpatterns = [
    url(r'^$', ControllerView.as_view(), name='form'),
]
