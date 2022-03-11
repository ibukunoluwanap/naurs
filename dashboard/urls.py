from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard_page'),
    # program
    path('program/', views.Program.as_view(), name='dashboard_program_page'),
    path('program/<int:pk>/', views.ProgramDetail.as_view(), name='dashboard_program_detail_page'),
    path('program/create/', views.ProgramCreate.as_view(), name='program_create_page'),
    # offer
    path('offer/', views.Offer.as_view(), name='dashboard_offer_page'),
    path('offer/<int:pk>/', views.OfferDetail.as_view(), name='dashboard_offer_detail_page'),
    path('offer/create/', views.OfferCreate.as_view(), name='dashboard_offer_create_page'),
]