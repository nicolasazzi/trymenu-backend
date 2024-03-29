
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('account.urls')),
    path('api/restaurant/', include('restaurant.urls')),
    path('api/search/', include('search.urls'))
]
