from django.contrib import messages
from .forms import OfferForm, FreeTrialOfferForm
from .models import OfferModel, FreeTrialOfferModel
from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView, DetailView

# offer view
class Offer(ListView):
    model = OfferModel
    template_name = "offer/offer.html"

# offer detail view
class OfferDetail(DetailView):
    model = OfferModel
    template_name = "offer/detail.html"
    context_object_name = "offer"


# freeTrial view
class FreeTrial(FormView):
    template_name = "components/notifications/popup-message.html"
    model = FreeTrialOfferModel
    form_class = FreeTrialOfferForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        user = form.save()
        messages.success(self.request, f"{user.name} successfully requested for free trial!")
        return super(FreeTrial, self).form_valid(form)
