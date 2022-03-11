from . import views
from django.urls import path

urlpatterns = [
    # offers
    path('', views.Offer.as_view(), name='offer_page'),
    path('<int:pk>/', views.OfferDetail.as_view(), name='offer_detail_page'),
    path('book_offer/<int:offer_id>/', views.BookOffer.as_view(), name='book_offer_page'),
    path('free_trial/', views.FreeTrial.as_view(), name='free_trial_page'),
]