from django.urls import path
from . import views

urlpatterns = [
    # dashboard
    path('', views.Dashboard.as_view(), name='dashboard_page'),
    # program
    path('program/', views.Program.as_view(), name='dashboard_program_page'),
    path('program/<int:pk>/', views.ProgramDetail.as_view(), name='dashboard_program_detail_page'),
    path('program/create/', views.ProgramCreate.as_view(), name='dashboard_program_create_page'),
    path('program/<int:pk>/update/', views.ProgramUpdate.as_view(), name='dashboard_program_update_page'),
    path('program/<int:program_id>/benefit/create/', views.ProgramBenefitCreate.as_view(), name='dashboard_program_benefit_create_page'),
    path('program/<int:pk>/benefit/delete/', views.ProgramBenefitDelete.as_view(), name='dashboard_program_benefit_delete_page'),
    path('program/<int:program_id>/<str:visibility>/visibility/', views.ProgramVisibility.as_view(), name='dashboard_program_visibility_page'),
    path('program/<int:pk>/enquiry/', views.ProgramEnquiryDelete.as_view(), name='dashboard_program_enquiry_page'),
    # offer
    path('offer/', views.Offer.as_view(), name='dashboard_offer_page'),
    path('offer/<int:pk>/', views.OfferDetail.as_view(), name='dashboard_offer_detail_page'),
    path('offer/create/', views.OfferCreate.as_view(), name='dashboard_offer_create_page'),
    # instructor
    path('instructor/', views.Instructor.as_view(), name='dashboard_instructor_page'),
    path('instructor/<int:pk>/', views.InstructorDetail.as_view(), name='dashboard_instructor_detail_page'),
    path('instructor/create/', views.InstructorCreate.as_view(), name='dashboard_instructor_create_page'),
    # student
    path('student/', views.Student.as_view(), name='dashboard_student_page'),
    path('student/<int:pk>/', views.StudentDetail.as_view(), name='dashboard_student_detail_page'),
    path('student/create/', views.StudentCreate.as_view(), name='dashboard_student_create_page'),
    # admin
    path('admin/', views.Admin.as_view(), name='dashboard_admin_page'),
    path('admin/<int:pk>/', views.AdminDetail.as_view(), name='dashboard_admin_detail_page'),
    path('admin/create/', views.AdminCreate.as_view(), name='dashboard_admin_create_page'),
    # about
    path('about/', views.About.as_view(), name='dashboard_about_page'),
    path('about/<int:pk>/', views.AboutDetail.as_view(), name='dashboard_about_detail_page'),
    path('about/create/', views.AboutCreate.as_view(), name='dashboard_about_create_page'),
    # home
    path('home/', views.Home.as_view(), name='dashboard_home_page'),
    path('home/<int:pk>/', views.HomeDetail.as_view(), name='dashboard_home_detail_page'),
    path('home/create/', views.HomeCreate.as_view(), name='dashboard_home_create_page'),
    # account
    path('account/', views.AccountDetail.as_view(), name='dashboard_account_detail_page'),
]