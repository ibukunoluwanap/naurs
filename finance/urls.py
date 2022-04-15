from django.urls import path
from . import views

urlpatterns = [
    # programs
    path('', views.Finance.as_view(), name='finance_page'),
    path('create/', views.BillingAddressCreate.as_view(), name='billing_address_create_page'),
]