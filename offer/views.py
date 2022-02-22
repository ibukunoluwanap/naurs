from django.contrib import messages
from .forms import BookOfferForm, FreeTrialOfferForm
from .models import BookOfferModel, OfferModel, FreeTrialOfferModel
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

# book offer view
class BookOffer(FormView):
    template_name = "offer/detail.html"
    model = BookOfferModel
    form_class = BookOfferForm
    success_url = 'offer_page'

    def form_valid(self, form):
        offer = OfferModel.objects.get(id=self.kwargs['offer_id'])
        user = form.save()
        user.offer = offer
        messages.success(self.request, f"{user.name} successfully booked {user.offer.title}!")
        return super(BookOffer, self).form_valid(form)

# freeTrial view
class FreeTrial(FormView):
    template_name = "components/notifications/popup-message.html"
    model = FreeTrialOfferModel
    form_class = FreeTrialOfferForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f"{user.name} successfully requested for free trial!")
        return super(FreeTrial, self).form_valid(form)
