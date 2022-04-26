import json
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from finance.forms import BillingAddressForm
from finance.models import BillingAddressModel, OrderModel, WalletModel
from django.contrib import messages
from offer.models import FreeTrialOfferModel
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from program.models import ProgramModel

# order view
class Order(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "dashboard/full_student_dashboard/order.html"
    login_url = 'login_page'
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.studentmodel)
        except:
            return (self.request.user.is_admin)

    def get(self, request):
        FreeTrialOfferModel.objects.filter(created_on__lte=datetime.now(timezone.utc)-timezone.timedelta(days=7)).update(is_active=False)
        return render(request, self.template_name)

# billing address create view
class BillingAddressCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = BillingAddressModel
    login_url = 'login_page'
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.studentmodel)
        except:
            return (self.request.user.instructormodel)

    def post(self, request, *args, **kwargs):
        context = {}
        context["billing_address_from"] = billing_address_from = BillingAddressForm(request.POST, request.FILES)

        if billing_address_from.is_valid():
            new_billing_address = billing_address_from.save(commit=False)
            print("B:",request.user)
            new_billing_address.user = request.user
            new_billing_address.save()
            messages.success(self.request, f"Successfully added billing address! <b>You can now purchase packages and classes</b>")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        for field in billing_address_from:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# top up wallet
@csrf_exempt
def top_up_wallet_session(request, amount):
    billing_address = get_object_or_404(BillingAddressModel, user=request.user)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    amount_int = int(amount)

    # creating stripe customer
    stripe_customer = stripe.Customer.create(
        address = {
            'city': billing_address.city_town,
            'country': billing_address.country,
            'line1': billing_address.street_address,
            'postal_code': billing_address.zip_code
        },
        email = request.user.email,
        name = request.user.get_full_name(),
    )

    wallet_session = stripe.checkout.Session.create(
        customer = stripe_customer.id,
        payment_method_types = ['card'],
        mode = 'payment',
        success_url = request.build_absolute_uri(reverse('top_up_wallet_success')) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url = request.build_absolute_uri(reverse('top_up_wallet_failed')),
        line_items = [
            {
                'price_data': {
                    'currency': 'aed',
                    'product_data': {
                    'name': "Wallet Top Up",
                    },
                    'unit_amount': int(amount_int * 100),
                },
                'quantity': 1,
            }
        ],
    )

    return JsonResponse({'sessionId': wallet_session.id})
  
class TopUpWalletPaymentSuccess(TemplateView):
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        wallet = get_object_or_404(WalletModel, user=request.user)
        new_wallet_balance = wallet.balance + int(session.amount_total / 100)
        wallet.balance = new_wallet_balance
        wallet.save()
        messages.success(request, 'Payment successful! Your account has been topped up.')
        return redirect('student_dashboard_page')

class TopUpWalletPaymentFailed(TemplateView):
    def get(self, request, *args, **kwargs):
        messages.error(request, 'Something went wrong during the payment processing! If your account was deducted please wait for n\
                        reverse within 24hrs. If still no progress, contact us and your bank. Thank you.')
        return redirect('student_dashboard_page')
