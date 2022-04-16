from django.urls import path
from . import views

urlpatterns = [
    path('', views.Finance.as_view(), name='finance_page'),
    path('create/', views.BillingAddressCreate.as_view(), name='billing_address_create_page'),
    path('stripe_config/', views.stripe_config, name='stripe_config_page'),
    path('payment_success/', views.PaymentSuccess.as_view(), name='payment_success'),
    path('payment_failed/', views.PaymentFailed.as_view(), name='payment_failed'),
    path('payment_history/', views.OrderHistory.as_view(), name='payment_history'),
    path('payment/checkout_session/<id>/', views.create_checkout_session, name='payment_checkout_session'),
]