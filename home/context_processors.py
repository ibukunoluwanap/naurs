from account.forms import RegisterForm, LoginForm
from instructor.models import InstructorModel
from about.models import AboutModel
from program.forms import ProgramEnquiryForm
from program.models import ProgramModel
from offer.models import OfferModel, BookOfferModel
from offer.forms import OfferForm, BookOfferForm, FreeTrialOfferForm

def global_context(request):
    context = {}
    # context['num_of_parks'] = Park.objects.all().count()
    # context['last_10_parks'] = Park.objects.order_by("-id")[:10]
    # context['parks_list'] =  json.dumps(list(Park.objects.order_by("-id").values()), cls=DjangoJSONEncoder)

    # all get
    context['offers'] = OfferModel.objects.order_by("-id")
    context['book_offers'] = BookOfferModel.objects.order_by("-id")
    context['instructors'] = InstructorModel.objects.order_by("-id")
    context['programs'] = ProgramModel.objects.order_by("-id")

    # last get
    context['last_10_offers'] = OfferModel.objects.order_by("-id")[:10]
    context['last_10_book_offers'] = BookOfferModel.objects.order_by("-id")[:10]
    context['last_4_instructors'] = InstructorModel.objects.order_by("-id")[:4]
    context['last_4_programs'] = ProgramModel.objects.order_by("-id")[:4]
    context['last_about'] = AboutModel.objects.order_by("-id")[:1]

    # offers
    context['free_offer_form'] = FreeTrialOfferForm()
    context['offer_form'] = OfferForm()
    context['book_offer_form'] = BookOfferForm()
    # authentication
    context['register_form'] = RegisterForm()
    context['login_form'] = LoginForm()
    # programs
    context['program_enquiry_form'] = ProgramEnquiryForm()
    return context