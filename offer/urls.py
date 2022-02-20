from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # offers
    path('free_trial/', views.FreeTrial.as_view(), name='free_trial_page'),
]