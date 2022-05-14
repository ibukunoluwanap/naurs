from django.urls import path
from . import views

urlpatterns = [
    # dashboard
    path('', views.Dashboard.as_view(), name='dashboard_page'),
    path('studio/', views.Studio.as_view(), name='dashboard_studio_page'),
    # program
    path('program/', views.Program.as_view(), name='dashboard_program_page'),
    path('program/<int:pk>/', views.ProgramDetail.as_view(), name='dashboard_program_detail_page'),
    path('program/create/', views.ProgramCreate.as_view(), name='dashboard_program_create_page'),
    path('program/instructor/<int:pk>/create/', views.ProgramInstructorCreate.as_view(), name='dashboard_program_instructor_create_page'),
    path('program/<int:pk>/update/', views.ProgramUpdate.as_view(), name='dashboard_program_update_page'),
    path('program/<int:program_id>/benefit/create/', views.ProgramBenefitCreate.as_view(), name='dashboard_program_benefit_create_page'),
    path('program/<int:pk>/benefit/delete/', views.ProgramBenefitDelete.as_view(), name='dashboard_program_benefit_delete_page'),
    path('program/<int:program_id>/<str:visibility>/visibility/', views.ProgramVisibility.as_view(), name='dashboard_program_visibility_page'),
    path('program/<int:pk>/enquiry/', views.ProgramEnquiryDelete.as_view(), name='dashboard_program_enquiry_page'),
    # calendar
    path('calendar/', views.CalendarDashboard.as_view(), name='dashboard_calendar_page'),
    path('calendar/create/', views.CalendarCreate.as_view(), name='dashboard_calendar_create_page'),
    path('calendar/duplicate/<int:pk>/', views.CalendarDuplicate.as_view(), name='dashboard_calendar_duplicate_page'),
    path('calendar/<int:pk>/delete/', views.CalendarDelete.as_view(), name='dashboard_calendar_delete_page'),
    # package
    path('package/', views.Package.as_view(), name='dashboard_package_page'),
    path('package/<int:pk>/', views.PackageDetail.as_view(), name='dashboard_package_detail_page'),
    path('package/create/', views.PackageCreate.as_view(), name='dashboard_package_create_page'),
    path('package/<int:pk>/update/', views.PackageUpdate.as_view(), name='dashboard_package_update_page'),
    path('package/<int:package_id>/<str:visibility>/visibility/', views.PackageVisibility.as_view(), name='dashboard_package_visibility_page'),
    # offer
    path('offer/', views.Offer.as_view(), name='dashboard_offer_page'),
    path('offer/<int:pk>/', views.OfferDetail.as_view(), name='dashboard_offer_detail_page'),
    path('offer/create/', views.OfferCreate.as_view(), name='dashboard_offer_create_page'),
    path('offer/<int:pk>/update/', views.OfferUpdate.as_view(), name='dashboard_offer_update_page'),
    path('offer/<int:pk>/book/', views.BookOfferDelete.as_view(), name='dashboard_book_offer_page'),
    path('offer/<int:offer_id>/<str:visibility>/visibility/', views.OfferVisibility.as_view(), name='dashboard_offer_visibility_page'),
    # free trial
    path('free_trial/', views.FreeTrial.as_view(), name='dashboard_free_trial_page'),
    # instructor
    path('instructor/', views.Instructor.as_view(), name='dashboard_instructor_page'),
    path('instructor/<int:pk>/', views.InstructorDetail.as_view(), name='dashboard_instructor_detail_page'),
    path('instructor/create/', views.InstructorCreate.as_view(), name='dashboard_instructor_create_page'),
    path('instructor/<int:pk>/update/', views.InstructorUpdate.as_view(), name='dashboard_instructor_update_page'),
    path('instructor/<int:instructor_id>/<str:visibility>/visibility/', views.InstructorVisibility.as_view(), name='dashboard_instructor_visibility_page'),
    # student
    path('student/', views.Student.as_view(), name='dashboard_student_page'),
    path('student/<int:pk>/', views.StudentDetail.as_view(), name='dashboard_student_detail_page'),
    path('student/create/', views.StudentCreate.as_view(), name='dashboard_student_create_page'),
    path('student/<int:pk>/update/', views.StudentUpdate.as_view(), name='dashboard_student_update_page'),
    path('student/<int:student_id>/<str:visibility>/visibility/', views.StudentVisibility.as_view(), name='dashboard_student_visibility_page'),
    # admin
    path('admin/', views.Admin.as_view(), name='dashboard_admin_page'),
    path('admin/<int:pk>/', views.AdminDetail.as_view(), name='dashboard_admin_detail_page'),
    path('admin/create/', views.AdminCreate.as_view(), name='dashboard_admin_create_page'),
    path('admin/<int:pk>/update/', views.AdminUpdate.as_view(), name='dashboard_admin_update_page'),
    path('admin/<int:admin_id>/<str:visibility>/visibility/', views.AdminVisibility.as_view(), name='dashboard_admin_visibility_page'),
    # users
    path('users/', views.Users.as_view(), name='dashboard_users_page'),
    path('users/<int:user_id>/<str:visibility>/visibility/', views.UsersVisibility.as_view(), name='dashboard_users_visibility_page'),
    # about
    path('about/', views.About.as_view(), name='dashboard_about_page'),
    path('about/<int:pk>/', views.AboutDetail.as_view(), name='dashboard_about_detail_page'),
    path('about/create/', views.AboutCreate.as_view(), name='dashboard_about_create_page'),
    path('about/<int:pk>/update/', views.AboutUpdate.as_view(), name='dashboard_about_update_page'),
    path('about/<int:pk>/delete/', views.AboutDelete.as_view(), name='dashboard_about_delete_page'),
    # home
    path('home/', views.Home.as_view(), name='dashboard_home_page'),
    path('home/<int:pk>/', views.HomeDetail.as_view(), name='dashboard_home_detail_page'),
    path('home/create/', views.HomeCreate.as_view(), name='dashboard_home_create_page'),
    path('home/<int:pk>/update/', views.HomeUpdate.as_view(), name='dashboard_home_update_page'),
    path('home/<int:pk>/delete/', views.HomeDelete.as_view(), name='dashboard_home_delete_page'),
    # account
    path('account/', views.AccountDetail.as_view(), name='dashboard_account_detail_page'),
    path('account/password/change/', views.AccountChangePassword.as_view(), name='dashboard_account_change_password_page'),
    path('account/<int:pk>/delete/', views.AccountDelete.as_view(), name='dashboard_account_delete_page'),
    # order
    path('order/', views.Order.as_view(), name='dashboard_order_page'),



    # student dashboard
    path('student_dashboard/', views.StudentDashboard.as_view(), name='student_dashboard_page'),
    path('student_dashboard/account/', views.StudentAccountDetail.as_view(), name='student_dashboard_account_page'),
    path('student_dashboard/account/password/change/', views.StudentAccountChangePassword.as_view(), name='student_account_change_password_page'),
    path('student_dashboard/package/', views.StudentPackage.as_view(), name='student_dashboard_package_page'),
    path('student_dashboard/get_package/<int:package_id>/<package_type>/', views.GetStudentPackage.as_view(), name='student_get_package'),
    path('student_dashboard/get_ticket/<int:order_id>/<ticket_type>/', views.GetPackageTicket.as_view(), name='student_get_ticket'),
    path('student_dashboard/calendar/', views.StudentCalendar.as_view(), name='student_calendar_page'),
]