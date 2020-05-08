from django.urls import path
from .views import registration_view

from rest_framework.authtoken import views


urlpatterns = [
    path('register/', registration_view),
    path('login/', views.obtain_auth_token),
]
