from re import template
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('administrator/', admin.site.urls),
    path('account/', include('account.urls')),
    path('', include('home.urls')),
    path('program/', include('program.urls')),
    path('about/', include('about.urls')),
    path('contact/', include('contact.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('offer/', include('offer.urls')),
    path('instructor/', include('instructor.urls')),
]

admin.site.site_header  =  "Test Admin Dashboard"  
admin.site.site_title  =  "Test Admin Dashboard"
admin.site.index_title  =  "Test Admin Dashboard"

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)