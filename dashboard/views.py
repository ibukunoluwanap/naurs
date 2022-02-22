from django.shortcuts import render
from offer.forms import OfferForm
from django.contrib import messages
from offer.models import OfferModel
from django.views.generic import View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

# dashboard list view
class Dashboard(LoginRequiredMixin, View):
    template_name = "dashboard/dashboard.html"
    login_url = 'login_page'

    def get(self, request):
        return render(request, self.template_name)

class OfferCreate(LoginRequiredMixin, CreateView):
    model = OfferModel
    form_class = OfferForm
    template_name = "dashboard/offer/create.html"
    login_url = 'login_page'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, f"Successfully created an offer!")
        return super(OfferCreate, self).form_valid(form)