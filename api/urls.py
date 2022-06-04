from . import views
from django.urls import path
from knox import views as knox_views

urlpatterns = [
    # auth API
    path('user/', views.UserAPI.as_view(), name='user_api'),
    path('register/', views.RegisterAPI.as_view(), name='register_api'),
    path('login/', views.LoginAPI.as_view(), name='login_api'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout_api'),
    path('logout_all/', knox_views.LogoutAllView.as_view(), name='logout_all_api'),
    path('change_password/', views.ChangePasswordAPI.as_view(), name='change_password_api'),
    path('password_reset_confirm/<token>/', views.PasswordResetConfirmAPI.as_view(), name='password_reset_confirm_api'),

    # program API
    path('program/', views.ProgramAPI.as_view(), name='program_api'),

    # package API
    path('package/', views.PackageAPI.as_view(), name='package_api'),

    # calendar API
    path('calendar/', views.CalendarAPI.as_view(), name='calendar_api'),

    # wallet update API
    path('wallet_update/', views.WalletUpdateAPI.as_view(), name='wallet_update_api'),

    # student update API
    path('get_package/<package_id>/', views.GetPackageAPI.as_view(), name='get_package_api'),

    # billing_address update API
    path('billing_address_update/', views.BillingAddressUpdateAPI.as_view(), name='billing_address_update_api'),

    # order API
    path('order/', views.OrderAPI.as_view(), name='order_api'),

    # transaction_history API
    path('transaction_history/', views.TransactionHistoryAPI.as_view(), name='transaction_history_api'),

    # student update API
    path('student_update/', views.StudentUpdateAPI.as_view(), name='student_update_api'),

    # instructor API
    path('instructor/', views.InstructorAPI.as_view(), name='instructor_api'),

    # instructor update API
    path('instructor_update/', views.InstructorUpdateAPI.as_view(), name='instructor_update_api'),

    # instructor notification create API
    path('instructor_notification_create/', views.InstructorNotificationCreateAPI.as_view(), name='instructor_notification_create_api'),

    # instructor notification API
    path('instructor_notification/', views.InstructorNotificationAPI.as_view(), name='instructor_notification_api'),

    # notification API
    path('notification/', views.NotificationAPI.as_view(), name='notification_api'),

    # ticket API
    path('ticket/', views.TicketAPI.as_view(), name='ticket_api'),

    # ticket create API
    path('ticket_create/<order_id>/<ticket_type>/', views.TicketCreateAPI.as_view(), name='ticket_create_api'),
]