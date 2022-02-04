from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='register_page'),
    path('login/', views.Login.as_view(), name='login_page'),
    path('forget_password/', views.ForgetPassword.as_view(), name='forget_password_page'),
]