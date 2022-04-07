from django.urls import path
from . import views

urlpatterns = [
    # programs
    path('', views.Program.as_view(), name='program_page'),
    path('<int:pk>/', views.ProgramDetail.as_view(), name='program_detail_page'),
    path('enquiry/<int:program_id>/', views.ProgramEnquiry.as_view(), name='program_enquiry_page'),
    # package
    path('package/', views.Package.as_view(), name='package_page'),
    path('package/<int:pk>/', views.PackageDetail.as_view(), name='package_detail_page'),
]