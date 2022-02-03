from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('dev_admin/', admin.site.urls),
    path('', include('home.urls')),
    path('account/', include('account.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)