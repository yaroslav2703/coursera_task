from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import AddItemView, GetItemView, PostReviewView

urlpatterns = [
    path('api/v1/goods/', csrf_exempt(AddItemView.as_view())),
    path('api/v1/goods/<int:item_id>/', csrf_exempt(GetItemView.as_view())),
    path('api/v1/goods/<int:item_id>/reviews/', csrf_exempt(PostReviewView.as_view())),
]
