from django.shortcuts import render
from django.contrib import messages
from .forms import OfferForm, FreeTrialOfferForm
from .models import OfferModel, FreeTrialOfferModel
from django.views.generic import FormView, View
from django.shortcuts import render, redirect

# offer view
class Offer(View):
    template_name = "offer/offer.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        context = {}
        context["offer_form"] = offer_form = OfferForm(request.POST)

        if offer_form.is_valid():
            # saving to database
            user = offer_form.save()
            messages.success(request, "Successfully added an offer!")
            return redirect('home_page')
        return render(request, self.template_name, context)

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
