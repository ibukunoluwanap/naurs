from django.urls import path
from . import views

urlpatterns = [
    # programs
    path('', views.Program.as_view(), name='program_page'),
    path('<int:pk>/', views.ProgramDetail.as_view(), name='program_detail_page'),
    path('enquiry/<int:program_id>/', views.ProgramEnquiry.as_view(), name='program_enquiry_page'),
]