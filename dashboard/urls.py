from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard_page'),
    path('offer/create/', views.OfferCreate.as_view(), name='offer_create_page'),
]