import json
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from pkg_resources import require
from finance.forms import BillingAddressForm
from finance.models import BillingAddressModel, OrderModel
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

# configuring stripe
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request, id):
    program = get_object_or_404(ProgramModel, pk=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment_success')) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('payment_failed')),
        line_items=[
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

    # return JsonResponse({'data': checkout_session})
    return JsonResponse({'sessionId': checkout_session.id})


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
        return render(request, self.template_name)

class PaymentFailed(TemplateView):
    template_name = "finance/payment/payment_failed.html"

class OrderHistory(ListView):
    model = OrderModel
    template_name = "finance/payment/order_history.html"