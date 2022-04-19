from django.urls import path
from . import views

urlpatterns = [
    path('', views.Finance.as_view(), name='finance_page'),
    path('create/', views.BillingAddressCreate.as_view(), name='billing_address_create_page'),

    path('payment/checkout_session/<id>/', views.create_checkout_session, name='payment_checkout_session'),
    path('payment_success/', views.PaymentSuccess.as_view(), name='payment_success'),
    path('payment_failed/', views.PaymentFailed.as_view(), name='payment_failed'),
    path('payment_history/', views.OrderHistory.as_view(), name='payment_history'),

    path('payment/top_up_wallet_session/<amount>/', views.top_up_wallet_session, name='top_up_wallet_session'),
    path('top_up_wallet_success/', views.TopUpWalletPaymentSuccess.as_view(), name='top_up_wallet_success'),
    path('top_up_wallet_failed/', views.TopUpWalletPaymentFailed.as_view(), name='top_up_wallet_failed'),
    path('top_up_wallet_history/', views.OrderHistory.as_view(), name='top_up_wallet_history'),
]