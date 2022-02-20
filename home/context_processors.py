from offer.forms import FreeTrialOfferForm

def global_context(request):
    context = {}
    # context['num_of_parks'] = Park.objects.all().count()
    # context['last_10_parks'] = Park.objects.order_by("-id")[:10]
    # context['parks_list'] =  json.dumps(list(Park.objects.order_by("-id").values()), cls=DjangoJSONEncoder)

    context['free_offer_form'] = FreeTrialOfferForm()
    return context