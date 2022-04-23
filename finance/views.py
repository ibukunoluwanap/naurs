import json
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from pkg_resources import require
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
# from django.contrib.sites.models import Site

# finance list view
class Finance(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "dashboard/full_student_dashboard/finance.html"
    login_url = 'login_page'
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.studentmodel)
        except:
            return (self.request.user.instructormodel)

    def get(self, request):
        FreeTrialOfferModel.objects.filter(created_on__lte=datetime.now(timezone.utc)-timezone.timedelta(days=7)).update(is_active=False)
        return render(request, self.template_name)

# billing address create view
class BillingAddressCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = BillingAddressModel
    login_url = 'login_page'
    template_name = "dashboard/full_student_dashboard/finance.html"
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
            return redirect("finance_page")
        for field in billing_address_from:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return render(request, self.template_name, context)

@csrf_exempt
def create_checkout_session(request, id):
    program = get_object_or_404(ProgramModel, pk=id)
    billing_address = get_object_or_404(BillingAddressModel, user=request.user)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
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

    checkout_session = stripe.checkout.Session.create(
        customer = stripe_customer.id,
        payment_method_types = ['card'],
        mode = 'payment',
        success_url = request.build_absolute_uri(reverse('payment_success')) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url = request.build_absolute_uri(reverse('payment_failed')),
        line_items = [
            {
                'price_data': {
                    'currency': 'aed',
                    'product_data': {
                    'name': program.title,
                    },
                    'unit_amount': int(program.price * 100),
                },
                'quantity': 1,
            }
        ],
    )

    # create order
    OrderModel.objects.create(
        user = request.user,
        program = program,
        stripe_payment_intent = checkout_session['payment_intent'],
        amount = program.price
    )

    # update program total space
    program.total_space = program.total_space - 1
    program.save()

    return JsonResponse({'sessionId': checkout_session.id})

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
    
class PaymentSuccess(TemplateView):
    template_name = "finance/payment/payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        order = get_object_or_404(OrderModel, stripe_payment_intent=session.payment_intent)
        order.status = True
        order.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/finance/'))

class PaymentFailed(TemplateView):
    template_name = "finance/payment/payment_failed.html"

class OrderHistory(ListView):
    model = OrderModel
    template_name = "finance/payment/order_history.html"


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
