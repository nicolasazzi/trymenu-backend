from django.urls import path
from .views import restaurants_request_view


urlpatterns = [
    path('get_restaurants/', restaurants_request_view),
]
