from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home_page'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('privacy_policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
]