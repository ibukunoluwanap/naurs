from account.forms import RegisterForm, LoginForm, User
from instructor.models import InstructorModel
from about.models import AboutModel
from program.forms import ProgramBenefitForm, ProgramBenefitInlineFormset, ProgramEnquiryForm, ProgramForm, ProgramPaymentForm
from program.models import ProgramBenefitModel, ProgramEnquiryModel, ProgramModel, ProgramPaymentModel
from offer.models import OfferModel, BookOfferModel
from offer.forms import OfferForm, BookOfferForm, FreeTrialOfferForm

def global_context(request):
    context = {}
    # programs with activate filter
    context['programs'] = ProgramModel.objects.filter(is_active=True).order_by("-id")
    context['last_10_programs'] = ProgramModel.objects.filter(is_active=True).order_by("-id")[:10]
    context['last_4_programs'] = ProgramModel.objects.filter(is_active=True).order_by("-id")[:4]
    # programs without activate filter
    context['without_filter_programs'] = ProgramModel.objects.order_by("-id")
    context['without_filter_last_10_programs'] = ProgramModel.objects.order_by("-id")[:10]
    context['without_filter_last_4_programs'] = ProgramModel.objects.order_by("-id")[:4]
    context['program_benefit'] = ProgramBenefitModel()
    # form
    context['program_form'] = ProgramForm()
    context['program_benefit_form'] = ProgramBenefitForm()
    context['program_benefit_inline_formset'] = ProgramBenefitInlineFormset()

    # all get
    context['offers'] = OfferModel.objects.order_by("-id")
    context['book_offers'] = BookOfferModel.objects.order_by("-id")
    context['instructors'] = InstructorModel.objects.order_by("-id")
    context['program_enquiries'] = ProgramEnquiryModel.objects.order_by("-id")
    context['program_payments'] = ProgramPaymentModel.objects.order_by("-id")
    context['users'] = User.objects.all()
    context['students'] = User.objects.filter(student=True)

    # last get
    context['last_10_offers'] = OfferModel.objects.order_by("-id")[:10]
    context['last_10_book_offers'] = BookOfferModel.objects.order_by("-id")[:10]
    context['last_4_instructors'] = InstructorModel.objects.order_by("-id")[:4]
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
    context['program_payment_form'] = ProgramPaymentForm()
    return context
