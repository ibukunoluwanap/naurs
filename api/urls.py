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

    # billing_address update API
    path('billing_address_update/', views.BillingAddressUpdateAPI.as_view(), name='billing_address_update_api'),

    # order API
    path('order/', views.OrderAPI.as_view(), name='order_api'),

    # student update API
    path('student_update/', views.StudentUpdateAPI.as_view(), name='student_update_api'),
]