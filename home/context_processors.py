from account.forms import RegisterForm, LoginForm
from offer.models import OfferModel, BookOfferModel
from offer.forms import OfferForm, BookOfferForm, FreeTrialOfferForm

def global_context(request):
    context = {}
    # context['num_of_parks'] = Park.objects.all().count()
    # context['last_10_parks'] = Park.objects.order_by("-id")[:10]
    # context['parks_list'] =  json.dumps(list(Park.objects.order_by("-id").values()), cls=DjangoJSONEncoder)

    context['offers'] = OfferModel.objects.order_by("-id")
    context['book_offers'] = BookOfferModel.objects.order_by("-id")
    context['last_10_offers'] = OfferModel.objects.order_by("-id")[:10]
    context['last_10_book_offers'] = BookOfferModel.objects.order_by("-id")[:10]

    # offers
    context['free_offer_form'] = FreeTrialOfferForm()
    context['offer_form'] = OfferForm()
    context['book_offer_form'] = BookOfferForm()
    # authentication
    context['register_form'] = RegisterForm()
    context['login_form'] = LoginForm()
    return context