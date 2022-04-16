from django.conf import settings
from about.forms import AboutForm
from account.forms import RegisterForm, LoginForm, UpdateAdminForm, UpdatePasswordForm, UpdateUserForm, User
from finance.forms import BillingAddressForm
from finance.models import BillingAddressModel
from home.forms import CalendarForm, ListingForm
from home.models import ListingModel
from instructor.forms import InstructorForm
from instructor.models import InstructorModel
from about.models import AboutModel
from program.forms import PackageForm, ProgramBenefitForm, ProgramEnquiryForm, ProgramForm, ProgramInstructorForm
from program.models import PackageModel, ProgramBenefitModel, ProgramEnquiryModel, ProgramModel
from offer.models import FreeTrialOfferModel, OfferModel, BookOfferModel
from offer.forms import OfferForm, BookOfferForm, FreeTrialOfferForm
from student.forms import StudentForm
from student.models import StudentModel

def global_context(request):
    context = {}

    # stripe publishable key
    context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY

    # user
    context['users'] = User.objects.order_by("-id")
    # user form
    context['update_user_form'] = UpdateUserForm()
    context['update_user_form_list'] = list(UpdateUserForm())


    # admin
    context['admins'] = User.objects.filter(admin=True)
    # admin form
    context['update_admin_form'] = UpdateAdminForm()
    context['update_admin_form_list'] = list(UpdateAdminForm())


    # program with activate filter
    context['programs'] = ProgramModel.objects.filter(is_active=True).order_by("-id")
    context['last_10_programs'] = ProgramModel.objects.filter(is_active=True).order_by("-id")[:10]
    context['last_3_programs'] = ProgramModel.objects.filter(is_active=True).order_by("-id")[:3]
    # program without activate filter
    context['without_filter_programs'] = ProgramModel.objects.order_by("-id")
    context['without_filter_last_10_programs'] = ProgramModel.objects.order_by("-id")[:10]
    context['without_filter_last_3_programs'] = ProgramModel.objects.order_by("-id")[:4]
    context['program_benefit'] = ProgramBenefitModel()
    context['program_enquiries'] = ProgramEnquiryModel.objects.order_by("-id")
    # program form
    context['program_form'] = ProgramForm()
    context['program_form_list'] = list(ProgramForm())
    context['calendar_form'] = CalendarForm()
    context['program_benefit_form'] = ProgramBenefitForm()
    context['program_enquiry_form'] = ProgramEnquiryForm()


    # package
    context['packages'] = PackageModel.objects.filter(is_active=True).order_by("-id")
    context['without_filter_packages'] = PackageModel.objects.order_by("-id")
    # package form
    context['package_form'] = PackageForm()
    context['package_form_list'] = list(PackageForm())


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
    context['offer_form_list'] = list(OfferForm())
    context['book_offer_form'] = BookOfferForm()
    context['free_offer_form'] = FreeTrialOfferForm()

    
    # free trial
    context['without_filter_free_trial'] = FreeTrialOfferModel.objects.order_by("-id")


    # instructor
    try:
        context["instructor"] = instructor = InstructorModel.objects.get(user=request.user)
        context["instructor_students"] = StudentModel.objects.filter(instructor=instructor)
    except:
        pass

    context['instructors'] = InstructorModel.objects.order_by("-id")
    context['last_4_instructors'] = InstructorModel.objects.order_by("-id")[:4]
    # instructor form
    context['instructor_form'] = InstructorForm()
    context['program_instructor_form'] = ProgramInstructorForm()
    context['instructor_form_list'] = list(InstructorForm())


    # about
    context['about'] = AboutModel.objects.order_by("-id")
    context['last_about'] = AboutModel.objects.order_by("-id")[:1]
    # about form
    context['about_form'] = AboutForm()
    context['about_form_list'] = list(AboutForm())

    
    # home form
    context['listings'] = ListingModel.objects.order_by("-id")
    context['listing_form'] = ListingForm()
    context['listing_form_list'] = list(ListingForm())

    
    # student
    context['students'] = StudentModel.objects.order_by("-id")
    # student form
    context['student_form'] = StudentForm()
    context['student_form_list'] = list(StudentForm())


    # authentication
    context['register_form'] = RegisterForm()
    context['login_form'] = LoginForm()
    context['update_password_form'] = UpdatePasswordForm()


    # finance
    context['billing_addresses'] = BillingAddressModel.objects.order_by("-id")
    # finance form
    context['billing_address_form'] = BillingAddressForm()

    return context
