from django.urls import path
from .views import restaurants_request_view, try_item


urlpatterns = [
    path('get_restaurants/', restaurants_request_view),
    path('try_item/', try_item),
]
