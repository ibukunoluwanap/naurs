from re import template
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('dev_admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('', include('home.urls')),
    path('music/', include('music.urls')),
    path('art/', include('art.urls')),
    path('fitness/', include('fitness.urls')),
    path('about/', include('about.urls')),
    path('contact/', include('contact.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('offer/', include('offer.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)