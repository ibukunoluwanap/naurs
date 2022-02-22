from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # offers
    path('', views.Offer.as_view(), name='offer_page'),
    path('<int:pk>/', views.OfferDetail.as_view(), name='offer_detail_page'),
    path('free_trial/', views.FreeTrial.as_view(), name='free_trial_page'),
]