from about.forms import AboutForm
from account.forms import RegisterForm, LoginForm, UpdateAdminForm, UpdatePasswordForm, UpdateUserForm, User
from home.forms import ListingForm
from home.models import ListingModel
from instructor.forms import InstructorForm
from instructor.models import InstructorModel
from about.models import AboutModel
from program.forms import ProgramBenefitForm, ProgramBenefitInlineFormset, ProgramEnquiryForm, ProgramForm, ProgramPaymentForm
from program.models import ProgramBenefitModel, ProgramEnquiryModel, ProgramModel, ProgramPaymentModel
from offer.models import OfferModel, BookOfferModel
from offer.forms import OfferForm, BookOfferForm, FreeTrialOfferForm

def global_context(request):
    context = {}
    # user
    context['users'] = User.objects.all()
    # user form
    context['update_user_form'] = UpdateUserForm()
    context['update_admin_form'] = UpdateAdminForm()
    context['update_password_form'] = UpdatePasswordForm()
    
    # program with activate filter
    context['programs'] = ProgramModel.objects.filter(is_active=True).order_by("-id")
    context['last_10_programs'] = ProgramModel.objects.filter(is_active=True).order_by("-id")[:10]
    context['last_4_programs'] = ProgramModel.objects.filter(is_active=True).order_by("-id")[:4]
    # program without activate filter
    context['without_filter_programs'] = ProgramModel.objects.order_by("-id")
    context['without_filter_last_10_programs'] = ProgramModel.objects.order_by("-id")[:10]
    context['without_filter_last_4_programs'] = ProgramModel.objects.order_by("-id")[:4]
    context['program_benefit'] = ProgramBenefitModel()
    context['program_enquiries'] = ProgramEnquiryModel.objects.order_by("-id")
    context['program_payments'] = ProgramPaymentModel.objects.order_by("-id")
    # program form
    context['program_form'] = ProgramForm()
    context['program_benefit_form'] = ProgramBenefitForm()
    context['program_benefit_inline_formset'] = ProgramBenefitInlineFormset()
    context['program_enquiry_form'] = ProgramEnquiryForm()
    context['program_payment_form'] = ProgramPaymentForm()


    # offer with activate filter
    context['offers'] = OfferModel.objects.filter(is_active=True).order_by("-id")
    context['last_10_offers'] = OfferModel.objects.filter(is_active=True).order_by("-id")[:10]
    context['last_4_offers'] = OfferModel.objects.filter(is_active=True).order_by("-id")[:4]
    # offer without activate filter
    context['without_filter_offers'] = OfferModel.objects.order_by("-id")
    context['without_filter_last_10_offers'] = OfferModel.objects.order_by("-id")[:10]
    context['without_filter_last_4_offers'] = OfferModel.objects.order_by("-id")[:4]
    context['without_filter_book_offers'] = BookOfferModel.objects.order_by("-id")
    # offer form
    context['offer_form'] = OfferForm()
    context['book_offer_form'] = BookOfferForm()
    context['free_offer_form'] = FreeTrialOfferForm()


    # instructor
    context['instructors'] = InstructorModel.objects.order_by("-id")
    context['last_4_instructors'] = InstructorModel.objects.order_by("-id")[:4]
    # instructor form
    context['instructor_form'] = InstructorForm()


    # about
    context['about'] = AboutModel.objects.order_by("-id")
    context['last_about'] = AboutModel.objects.order_by("-id")[:1]
    # about form
    context['about_form'] = AboutForm()

    
    # home form
    context['listings'] = ListingModel.objects.order_by("-id")
    context['listing_form'] = ListingForm()

    
    # student
    context['students'] = User.objects.filter(student=True)


    # authentication
    context['register_form'] = RegisterForm()
    context['login_form'] = LoginForm()

    return context
