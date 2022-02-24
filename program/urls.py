from django.urls import path
from . import views

urlpatterns = [
    path('', views.Program.as_view(), name='program_page'),
]