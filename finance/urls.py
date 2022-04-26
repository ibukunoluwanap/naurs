from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.Order.as_view(), name='order_page'),
    path('create/', views.BillingAddressCreate.as_view(), name='billing_address_create_page'),
    path('payment/top_up_wallet_session/<amount>/', views.top_up_wallet_session, name='top_up_wallet_session'),
    path('top_up_wallet_success/', views.TopUpWalletPaymentSuccess.as_view(), name='top_up_wallet_success'),
    path('top_up_wallet_failed/', views.TopUpWalletPaymentFailed.as_view(), name='top_up_wallet_failed'),
]