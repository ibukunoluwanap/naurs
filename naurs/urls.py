from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('dev_admin/', admin.site.urls),
    path('', include('home.urls')),
    path('account/', include('account.urls')),
]
