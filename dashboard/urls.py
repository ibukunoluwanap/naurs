from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard_page'),
    path('program/', views.Program.as_view(), name='dashboard_program_page'),
    path('program/<int:pk>/', views.ProgramDetail.as_view(), name='dashboard_program_detail_page'),
    path('program/create/', views.ProgramCreate.as_view(), name='program_create_page'),
    path('offer/create/', views.OfferCreate.as_view(), name='offer_create_page'),
]