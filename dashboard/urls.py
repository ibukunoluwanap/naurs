from django.urls import path
from . import views

urlpatterns = [
    # dashboard
    path('', views.Dashboard.as_view(), name='dashboard_page'),
    # program
    path('program/', views.Program.as_view(), name='dashboard_program_page'),
    path('program/<int:pk>/', views.ProgramDetail.as_view(), name='dashboard_program_detail_page'),
    path('program/create/', views.ProgramCreate.as_view(), name='dashboard_program_create_page'),
    # offer
    path('offer/', views.Offer.as_view(), name='dashboard_offer_page'),
    path('offer/<int:pk>/', views.OfferDetail.as_view(), name='dashboard_offer_detail_page'),
    path('offer/create/', views.OfferCreate.as_view(), name='dashboard_offer_create_page'),
    # instructor
    path('instructor/', views.Instructor.as_view(), name='dashboard_instructor_page'),
    path('instructor/<int:pk>/', views.InstructorDetail.as_view(), name='dashboard_instructor_detail_page'),

    # about
    path('about/', views.About.as_view(), name='dashboard_about_page'),
    path('about/<int:pk>/', views.AboutDetail.as_view(), name='dashboard_about_detail_page'),
]