from django.shortcuts import render
from offer.forms import OfferForm
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