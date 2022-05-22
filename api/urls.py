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
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password_api'),
    path('password_reset_confirm/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm_api'),

    # program API
    path('program/', views.ProgramAPI.as_view(), name='program_api'),

    # package
    path('package/', views.PackageAPI.as_view(), name='package_api'),
]