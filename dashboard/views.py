from django.shortcuts import redirect, render
from offer.forms import OfferForm
from django.contrib import messages
from offer.models import OfferModel
from django.views.generic import View, ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from program.models import ProgramModel

# dashboard list view
class Dashboard(LoginRequiredMixin, View):
    template_name = "dashboard/dashboard.html"
    login_url = 'login_page'

    def get(self, request):
        return render(request, self.template_name)

# dashboard program view
class Program(LoginRequiredMixin, ListView):
    model = ProgramModel
    login_url = 'login_page'
    template_name = "dashboard/program/program.html"

# dashboard program detail view
class ProgramDetail(LoginRequiredMixin, DetailView):
    model = ProgramModel
    login_url = 'login_page'
    template_name = "dashboard/program/detail.html"
    context_object_name = "program"

class OfferCreate(LoginRequiredMixin, CreateView):
    model = OfferModel
    form_class = OfferForm
    template_name = "dashboard/offer/create.html"
    login_url = 'login_page'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        context = {}
        context["offer_form"] = offer_form = OfferForm(request.POST, request.FILES)

        if offer_form.is_valid():
            offer_form.save()
            messages.success(self.request, f"Successfully created an offer!")
            return redirect("offer_create_page")
        return render(request, self.template_name, context)