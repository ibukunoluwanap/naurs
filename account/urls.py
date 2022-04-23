from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # authentication
    path('verify_email/<uidb64>/<token>/', views.VerifyEmail.as_view(), name='verify_email'),
    path('register/', views.Register.as_view(), name='register_page'),
    path('login/', views.Login.as_view(), name='login_page'),
    path('logout/', views.Logout.as_view(), name='logout_page'),

    # forgot password
    path('forget_password/', auth_views.PasswordResetView.as_view(template_name="account/forgot_password.html", html_email_template_name="account/forgot_password_email.html", subject_template_name="account/forget_password_subject.txt"),  name='password_reset'),
    path('forget_password_done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('forget_password_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="account/forgot_password_confirm.html"), name='password_reset_confirm'),
    path('forget_password_complete/', views.PasswordResetComplete.as_view(), name="password_reset_complete"),
]