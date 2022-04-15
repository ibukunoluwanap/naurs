from django.shortcuts import redirect, render
from finance.forms import BillingAddressForm
from finance.models import BillingAddressModel, WalletModel
from django.contrib import messages
from offer.models import FreeTrialOfferModel
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from program.models import ProgramModel
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils import timezone
from datetime import datetime

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
