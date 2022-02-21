from django.shortcuts import render
from django.contrib import messages
from .forms import OfferForm, FreeTrialOfferForm
from .models import OfferModel, FreeTrialOfferModel
from django.views.generic import FormView
from django.shortcuts import render, redirect

# offer view
class Offer(FormView):
    template_name = "components/notifications/popup-message.html"
    model = OfferModel
    form_class = OfferForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        user = form.save()
        messages.success(self.request, f"{user.name} successfully requested for free trial!")
        return super(Offer, self).form_valid(form)

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
