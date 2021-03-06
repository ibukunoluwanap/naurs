from copy import deepcopy
from email.errors import HeaderParseError
import socket
import uuid
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from about.forms import AboutForm
from about.models import AboutModel
from account.forms import RegisterForm, UpdateAdminForm, UpdateUserForm
from finance.models import OrderModel, TicketModel, WalletModel
from home.forms import CalendarForm, ListingForm, NotificationForm, StudioUserForm
from home.models import CalendarModel, ListingModel, NotificationModel, StudioModel, StudioUserModel
from home.views import get_date, next_month, prev_month
from instructor.forms import InstructorForm, InstructorNotificationForm
from instructor.models import InstructorModel, InstructorNotificationModel
from naurs.settings import EMAIL_HOST_USER
from offer.forms import OfferForm
from django.contrib import messages
from offer.models import BookOfferModel, FreeTrialOfferModel, OfferModel
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from program.forms import PackageForm, ProgramBenefitForm, ProgramForm, ProgramInstructorForm
from program.models import PackageModel, ProgramBenefitModel, ProgramEnquiryModel, ProgramModel
from django.contrib.auth import get_user_model
from student.forms import StudentForm
from django.contrib.auth.mixins import UserPassesTestMixin
from student.models import StudentModel
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from home.utils import Calendar
from django.utils.safestring import mark_safe
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader

# setting User model
User = get_user_model()

# dashboard list view
class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "dashboard/dashboard.html"
    login_url = 'login_page'
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

    def get(self, request):
        context = {}
        labels = []
        data = []

        FreeTrialOfferModel.objects.filter(created_on__lte=datetime.now(timezone.utc)-timezone.timedelta(days=7)).update(is_active=False)

        programs = ProgramModel.objects.order_by("-id")
        for program in programs:
            labels.append(program.title)
            data.append(program.total_space)

        context["labels"] = labels
        context["data"] = data
        try:
            context["wallet"] = WalletModel.objects.get(user=request.user)
        except:
            pass
        return render(request, self.template_name, context)

# Studio list view
class Studio(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "dashboard/studio.html"
    login_url = 'login_page'
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get(self, request):
        return render(request, self.template_name)

# Studio user form
class StudioUserCreate(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = "dashboard/studio.html"
    model = StudioUserModel
    form_class = StudioUserForm
    success_url = '/dashboard/studio/'

    def test_func(self):
        return (self.request.user.is_admin)

    def form_valid(self, form):
        new_form = form.save(commit=False)
        studio = StudioModel.objects.get(id=self.kwargs['pk'])
        studio.is_active = True
        studio.save()
        new_form.studio = studio
        new_form.save()
        messages.success(self.request, f'Successfully added person to studio!')
        return super(StudioUserCreate, self).form_valid(form)

# Studio free list view
class StudioFree(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "dashboard/studio.html"
    login_url = 'login_page'
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get(self, request, pk):
        studio = StudioModel.objects.get(id=pk)
        studio.is_active = False
        studio.save()
        messages.success(self.request, f'Successfully <b>FREE</b> {studio}!')
        return redirect("dashboard_studio_page")

# dashboard program view
class Program(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ProgramModel
    login_url = 'login_page'
    template_name = "dashboard/program/program.html"
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

# dashboard program detail view
class ProgramDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ProgramModel
    login_url = 'login_page'
    template_name = "dashboard/program/detail.html"
    context_object_name = "program"
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

    def get_context_data(self, **kwargs):
        context = super(ProgramDetail, self).get_context_data(**kwargs)
        program = ProgramModel.objects.get(id=self.kwargs['pk'])
        context['program_form_with_instance'] = list(ProgramForm(instance=program))
        return context

# dashboard program create view
class ProgramCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = ProgramForm
    login_url = 'login_page'
    template_name = "dashboard/program/program.html"
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        context = {}
        context["program_form"] = program_form = ProgramForm(request.POST, request.FILES)

        if program_form.is_valid():
            program_form.save()
            messages.success(self.request, f"Successfully created a class!")
            return redirect("dashboard_program_page")
        for field in program_form:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return render(request, self.template_name, context)

# dashboard program Update view
class ProgramUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ProgramModel
    form_class = ProgramForm
    login_url = 'login_page'
    template_name = "dashboard/program/program.html"
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

    def get_success_url(self):
        messages.success(self.request, "Successfully updated class!")
        return reverse_lazy('dashboard_program_detail_page', kwargs={'pk': self.kwargs['pk']})

# dashboard program instructor create view
class ProgramInstructorCreate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = ProgramInstructorForm
    login_url = 'login_page'
    template_name = "dashboard/program/program.html"
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        context = {}
        context["program_instructor_form"] = program_instructor_form = ProgramInstructorForm(request.POST)

        if program_instructor_form.is_valid():
            instructors = program_instructor_form.cleaned_data.get("instructors")
            ProgramModel.objects.get(id=self.kwargs['pk']).instructors.add(*instructors)
            messages.success(self.request, f"Successfully added instructor to class!")
            return redirect('dashboard_program_detail_page', pk=self.kwargs['pk'])
        for field in program_instructor_form:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return render(request, self.template_name, context)

# dashboard program benefit create view
class ProgramBenefitCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = ProgramForm
    login_url = 'login_page'
    template_name = "dashboard/program/detail.html"
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        program = ProgramModel.objects.get(id=self.kwargs['program_id'])
        program_benefit_form = ProgramBenefitForm(request.POST)

        if program_benefit_form.is_valid():
            program_benefit = program_benefit_form.save(commit=False)
            program_benefit.program = program
            program_benefit.save()
            messages.success(self.request, f"Successfully added a program benefit!")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/dashboard/'))
        for field in program_benefit_form:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return redirect("dashboard_program_page")

# dashboard program benefit delete view
class ProgramBenefitDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ProgramBenefitModel
    login_url = 'login_page'
    template_name = "dashboard/program/detail.html"
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

    def get_success_url(self):
        messages.success(self.request, f"Successfully deleted program benefit!")
        return reverse_lazy('dashboard_program_detail_page', kwargs={'pk': self.kwargs['pk']})

# dashboard program visibility view
class ProgramVisibility(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'login_page'
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        program_id = self.kwargs['program_id']
        visibility = self.kwargs['visibility']
        program =ProgramModel.objects.get(id=program_id)
        if visibility == 'deactivate':
            if program.is_active:
                program.is_active = False
                program.save()
                messages.success(self.request, "Successfully deactivated class!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))
            program.is_active = True
            program.save()
            messages.success(self.request, "Successfully reactivated class!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))
        elif visibility == 'delete':
            program.delete()
            messages.success(self.request, "Successfully deleted class!")
            return redirect("dashboard_program_page")

# dashboard program enquiry delete view
class ProgramEnquiryDelete(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'login_page'
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        program_enquiry =ProgramEnquiryModel.objects.get(id=pk)
        program_enquiry.delete()
        messages.success(self.request, "Successfully deleted program enquiry!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))

# dashboard package view
class Package(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = PackageModel
    login_url = 'login_page'
    template_name = "dashboard/package/package.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

# dashboard package detail view
class PackageDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = PackageModel
    login_url = 'login_page'
    template_name = "dashboard/package/detail.html"
    context_object_name = "package"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get_context_data(self, **kwargs):
        context = super(PackageDetail, self).get_context_data(**kwargs)
        package = PackageModel.objects.get(id=self.kwargs['pk'])
        context['package_form_with_instance'] = list(PackageForm(instance=package))
        return context

# dashboard package create view
class PackageCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = PackageForm
    login_url = 'login_page'
    template_name = "dashboard/package/package.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        context = {}
        context["package_form"] = package_form = PackageForm(request.POST, request.FILES)

        if package_form.is_valid():
            package_form.save()
            messages.success(self.request, f"Successfully created a package!")
            return redirect("dashboard_package_page")
        for field in package_form:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return render(request, self.template_name, context)

# dashboard package Update view
class PackageUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PackageModel
    form_class = PackageForm
    login_url = 'login_page'
    template_name = "dashboard/package/package.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get_success_url(self):
        messages.success(self.request, "Successfully updated package!")
        return reverse_lazy('dashboard_package_detail_page', kwargs={'pk': self.kwargs['pk']})

# dashboard package visibility view
class PackageVisibility(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'login_page'
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        package_id = self.kwargs['package_id']
        visibility = self.kwargs['visibility']
        package =PackageModel.objects.get(id=package_id)
        if visibility == 'deactivate':
            if package.is_active:
                package.is_active = False
                package.save()
                messages.success(self.request, "Successfully deactivated package!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))
            package.is_active = True
            package.save()
            messages.success(self.request, "Successfully reactivated package!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))
        elif visibility == 'delete':
            package.delete()
            messages.success(self.request, "Successfully deleted package!")
            return redirect("dashboard_package_page")

# dashboard calendar view
class CalendarDashboard(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = PackageModel
    login_url = 'login_page'
    template_name = "dashboard/calendar/calendar.html"
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month, self.request.user)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

# dashboard  calendar create view
class CalendarCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = CalendarForm
    login_url = 'login_page'
    template_name = "dashboard/calendar/calendar.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        calendar_form = CalendarForm(request.POST)

        if calendar_form.is_valid():
            calendar_form.save()
            messages.success(self.request, f"Successfully added a class to calendar!")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/dashboard/calendar/'))
        for field in calendar_form:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return redirect("dashboard_calendar_page")

class CalendarDuplicate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = CalendarForm
    login_url = 'login_page'
    template_name = "dashboard/calendar/duplicate.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get(self, request, *args, **kwargs):
        context = {}
        calendar_id = self.kwargs['pk']
        context['calendar'] = calendar = CalendarModel.objects.get(id=calendar_id)
        context['calendar_form_with_instance'] = CalendarForm(instance=calendar)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        calendar_form = CalendarForm(request.POST)
        calendar_id = self.kwargs['pk']

        if calendar_form.is_valid():
            duplicate_calendar = deepcopy(CalendarModel.objects.get(id=calendar_id))
            duplicate_calendar.id = None
            duplicate_calendar.program = calendar_form.cleaned_data.get('program')
            duplicate_calendar.instructor = calendar_form.cleaned_data.get('instructor')
            duplicate_calendar.start_at = calendar_form.cleaned_data.get('start_at')
            duplicate_calendar.end_at = calendar_form.cleaned_data.get('end_at')
            duplicate_calendar.save()

            messages.success(self.request, f"Successfully added a class to calendar!")
            return redirect("dashboard_calendar_page")
        for field in calendar_form:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return redirect("dashboard_calendar_page")

# dashboard calendar delete view
class CalendarDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CalendarModel
    login_url = 'login_page'
    template_name = "dashboard/calendar/calendar.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get_success_url(self):
        messages.success(self.request, f"Successfully deleted class calendar!")
        return reverse_lazy('dashboard_calendar_page', kwargs={'pk': self.kwargs['pk']})

# dashboard offer view
class Offer(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = OfferModel
    login_url = 'login_page'
    template_name = "dashboard/offer/offer.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

# dashboard free trial view
class FreeTrial(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = FreeTrialOfferModel
    login_url = 'login_page'
    template_name = "dashboard/free_trial/free_trial.html"
    raise_exception = True

    def test_func(self):
        FreeTrialOfferModel.objects.filter(created_on__lte=datetime.now(timezone.utc)-timezone.timedelta(days=7)).update(is_active=False)
        return (self.request.user.is_admin)

# dashboard offer detail view
class OfferDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = OfferModel
    login_url = 'login_page'
    template_name = "dashboard/offer/detail.html"
    context_object_name = "offer"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get_context_data(self, **kwargs):
        context = super(OfferDetail, self).get_context_data(**kwargs)
        offer = OfferModel.objects.get(id=self.kwargs['pk'])
        context['offer_form_with_instance'] = list(OfferForm(instance=offer))
        return context

# dashboard offer create view
class OfferCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = OfferForm
    login_url = 'login_page'
    template_name = "dashboard/offer/offer.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        context = {}
        context["offer_form"] = offer_form = OfferForm(request.POST, request.FILES)

        if offer_form.is_valid():
            offer_form.save()
            messages.success(self.request, f"Successfully created an offer!")
            return redirect("dashboard_offer_page")
        for field in offer_form:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return render(request, self.template_name, context)

# dashboard offer create view
class OfferUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = OfferModel
    form_class = OfferForm
    login_url = 'login_page'
    template_name = "dashboard/offer/offer.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get_success_url(self):
        messages.success(self.request, "Successfully updated offer!")
        return reverse_lazy('dashboard_offer_detail_page', kwargs={'pk': self.kwargs['pk']})

# dashboard offer visibility view
class OfferVisibility(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'login_page'
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        offer_id = self.kwargs['offer_id']
        visibility = self.kwargs['visibility']
        offer = OfferModel.objects.get(id=offer_id)
        if visibility == 'deactivate':
            if offer.is_active:
                offer.is_active = False
                offer.save()
                messages.success(self.request, "Successfully deactivated offer!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))
            offer.is_active = True
            offer.save()
            messages.success(self.request, "Successfully reactivated offer!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))
        elif visibility == 'delete':
            offer.delete()
            messages.success(self.request, "Successfully deleted offer!")
            return redirect("dashboard_offer_page")

# dashboard offer booking delete view
class BookOfferDelete(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'login_page'
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        book_offer =BookOfferModel.objects.get(id=pk)
        book_offer.delete()
        messages.success(self.request, "Successfully deleted booked offer!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))

# dashboard instructor view
class Instructor(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = InstructorModel
    login_url = 'login_page'
    template_name = "dashboard/instructor/instructor.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

# dashboard instructor detail view
class InstructorDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = InstructorModel
    login_url = 'login_page'
    template_name = "dashboard/instructor/detail.html"
    context_object_name = "instructor"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get_context_data(self, **kwargs):
        context = super(InstructorDetail, self).get_context_data(**kwargs)
        instructor = InstructorModel.objects.get(id=self.kwargs['pk'])
        context['instructor_form_with_instance'] = list(InstructorForm(instance=instructor))
        context['update_user_form_with_instance'] = UpdateUserForm(instance=instructor.user)
        return context

# dashboard instructor create view
class InstructorCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = InstructorForm
    login_url = 'login_page'
    template_name = "dashboard/instructor/instructor.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        context = {}
        context["instructor_form"] = instructor_form = InstructorForm(request.POST)
        context["register_form"] = register_form = RegisterForm(request.POST)

        if instructor_form.is_valid() and register_form.is_valid():
            user=register_form.save(commit=False)
            user.staff = True;
            user.save()
            new_instructor = instructor_form.save(commit=False)
            new_instructor.user = user
            WalletModel.objects.create(user=new_instructor.user)
            new_instructor.save()
            messages.success(self.request, f"Successfully added an instructor!")
            return redirect("dashboard_instructor_page")
        if instructor_form.errors:
            for field in instructor_form:
                for error in field.errors:
                    messages.error(self.request, f"<b>{field.label}:</b> {error}")
        if register_form.errors:
            for field in register_form:
                for error in field.errors:
                    messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return render(request, self.template_name, context)

# dashboard instructor create view
class InstructorUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = InstructorModel
    form_class = InstructorForm
    login_url = 'login_page'
    template_name = "dashboard/instructor/instructor.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get_success_url(self):
        messages.success(self.request, "Successfully updated instructor!")
        return reverse_lazy('dashboard_instructor_detail_page', kwargs={'pk': self.kwargs['pk']})

# dashboard instructor visibility view
class InstructorVisibility(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'login_page'
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        instructor_id = self.kwargs['instructor_id']
        visibility = self.kwargs['visibility']
        instructor = InstructorModel.objects.get(id=instructor_id)
        if visibility == 'deactivate':
            if instructor.user.is_active:
                instructor.user.is_active = False
                instructor.user.save()
                messages.success(self.request, "Successfully deactivated instructor!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))
            instructor.user.is_active = True
            instructor.user.save()
            messages.success(self.request, "Successfully reactivated instructor!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))
        elif visibility == 'delete':
            instructor.user.delete()
            messages.success(self.request, "Successfully deleted instructor!")
            return redirect("dashboard_instructor_page")

# dashboard student view
class Student(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = StudentModel
    login_url = 'login_page'
    template_name = "dashboard/student/student.html"
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

# dashboard student detail view
class StudentDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = StudentModel
    login_url = 'login_page'
    template_name = "dashboard/student/detail.html"
    context_object_name = "student"
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

    def get_context_data(self, **kwargs):
        context = super(StudentDetail, self).get_context_data(**kwargs)
        student = StudentModel.objects.get(id=self.kwargs['pk'])
        context['student_form_with_instance'] = list(StudentForm(instance=student))
        context['update_user_form_with_instance'] = UpdateUserForm(instance=student.user)
        return context

# dashboard student create view
class StudentCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = StudentForm
    login_url = 'login_page'
    template_name = "dashboard/student/student.html"
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        context = {}
        context["student_form"] = student_form = StudentForm(request.POST)

        if student_form.is_valid():
            user = student_form.cleaned_data.get('user')
            if user.is_admin:
                messages.error(self.request, f"{user} is admin and cannot be student!")
                return redirect("dashboard_student_page")
            else:
                try:
                    if user.instructormodel:
                        messages.error(self.request, f"{user} is instructor and cannot be student!")
                        return redirect("dashboard_student_page")
                    elif user.studentmodel:
                        messages.info(self.request, f"{user} already a student!")
                        return redirect("dashboard_student_page")
                except:
                    student_form.save()
                    messages.success(self.request, f"Successfully added an student!")
                    return redirect("dashboard_student_page")
        for field in student_form:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return render(request, self.template_name, context)

# dashboard student create view
class StudentUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = StudentModel
    form_class = StudentForm
    login_url = 'login_page'
    template_name = "dashboard/student/student.html"
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

    def get_success_url(self):
        messages.success(self.request, "Successfully updated student!")
        return reverse_lazy('dashboard_student_detail_page', kwargs={'pk': self.kwargs['pk']})

# dashboard student visibility view
class StudentVisibility(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'login_page'
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        student_id = self.kwargs['student_id']
        visibility = self.kwargs['visibility']
        student = StudentModel.objects.get(id=student_id)
        if visibility == 'deactivate':
            if student.user.is_active:
                student.user.is_active = False
                student.user.save()
                messages.success(self.request, "Successfully deactivated student!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))
            student.user.is_active = True
            student.user.save()
            messages.success(self.request, "Successfully reactivated student!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))
        elif visibility == 'delete':
            student.user.delete()
            messages.success(self.request, "Successfully deleted student!")
            return redirect("dashboard_student_page")

# dashboard admin view
class Admin(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    login_url = 'login_page'
    template_name = "dashboard/admin/admin.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

# dashboard admin detail view
class AdminDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    login_url = 'login_page'
    template_name = "dashboard/admin/detail.html"
    context_object_name = "admin"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get_context_data(self, **kwargs):
        context = super(AdminDetail, self).get_context_data(**kwargs)
        admin = User.objects.get(id=self.kwargs['pk'], admin=True)
        context['admin_form_with_instance'] = list(UpdateAdminForm(instance=admin))
        return context

# dashboard admin create view
class AdminCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = UpdateAdminForm
    login_url = 'login_page'
    template_name = "dashboard/instructor/instructor.html"
    template_name = "dashboard/admin/admin.html"
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        context = {}
        context["admin_form"] = admin_form = UpdateAdminForm(request.POST, request.FILES)

        if admin_form.is_valid():
            new_admin = admin_form.save(commit=False)
            new_admin.admin = True
            new_admin.staff = False
            new_admin.save()
            messages.success(self.request, f"Successfully added an admin!")
            return redirect("dashboard_admin_page")
        for field in admin_form:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return render(request, self.template_name, context)

# dashboard admin create view
class AdminUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UpdateAdminForm
    login_url = 'login_page'
    template_name = "dashboard/instructor/instructor.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get_success_url(self):
        messages.success(self.request, "Successfully updated admin!")
        return reverse_lazy('dashboard_admin_detail_page', kwargs={'pk': self.kwargs['pk']})

# dashboard admin visibility view
class AdminVisibility(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'login_page'
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        admin_id = self.kwargs['admin_id']
        visibility = self.kwargs['visibility']
        admin = User.objects.get(id=admin_id)
        if visibility == 'deactivate':
            if admin.is_active:
                admin.is_active = False
                admin.save()
                messages.success(self.request, "Successfully deactivated admin!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))
            admin.is_active = True
            admin.save()
            messages.success(self.request, "Successfully reactivated admin!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))
        elif visibility == 'delete':
            admin.delete()
            messages.success(self.request, "Successfully deleted admin!")
            return redirect("dashboard_admin_page")

# dashboard user view
class Users(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    login_url = 'login_page'
    template_name = "dashboard/users/users.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

# dashboard users visibility view
class UsersVisibility(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'login_page'
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_authenticated)

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        visibility = self.kwargs['visibility']
        user = User.objects.get(id=user_id)
        if visibility == 'deactivate':
            if user.is_active:
                if request.user.is_admin:
                    user.is_active = False
                    user.save()
                    messages.success(self.request, "Successfully deactivated user!")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))
                user.is_active = False
                user.save()
                messages.success(self.request, "Successfully deactivated user!")
                return redirect("login_page")
            user.is_active = True
            user.save()
            messages.success(self.request, "Successfully reactivated user!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))
        elif visibility == 'delete':
            user.delete()
            messages.success(self.request, "Successfully deleted user!")
            return redirect("dashboard_users_page")

# dashboard about view
class About(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = AboutModel
    login_url = 'login_page'
    template_name = "dashboard/about/about.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

# dashboard about detail view
class AboutDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = AboutModel
    login_url = 'login_page'
    template_name = "dashboard/about/detail.html"
    context_object_name = "about"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get_context_data(self, **kwargs):
        context = super(AboutDetail, self).get_context_data(**kwargs)
        about = AboutModel.objects.get(id=self.kwargs['pk'])
        context['about_form_with_instance'] = list(AboutForm(instance=about))
        return context

# dashboard about create view
class AboutCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = AboutForm
    login_url = 'login_page'
    template_name = "dashboard/about/about.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        context = {}
        context["about_form"] = about_form = AboutForm(request.POST, request.FILES)

        if about_form.is_valid():
            about_form.save()
            messages.success(self.request, f"Successfully added an about!")
            return redirect("dashboard_about_page")
        for field in about_form:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return render(request, self.template_name, context)

# dashboard about create view
class AboutUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AboutModel
    form_class = AboutForm
    login_url = 'login_page'
    template_name = "dashboard/about/about.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get_success_url(self):
        messages.success(self.request, "Successfully updated about!")
        return reverse_lazy('dashboard_about_detail_page', kwargs={'pk': self.kwargs['pk']})

# dashboard about delete view
class AboutDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AboutModel
    login_url = 'login_page'
    template_name = "dashboard/about/detail.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get_success_url(self):
        messages.success(self.request, "Successfully deleted about!")
        return reverse_lazy('dashboard_about_page')

# dashboard home view
class Home(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ListingModel
    login_url = 'login_page'
    template_name = "dashboard/home/home.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

# dashboard home detail view
class HomeDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ListingModel
    login_url = 'login_page'
    template_name = "dashboard/home/detail.html"
    context_object_name = "listing"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get_context_data(self, **kwargs):
        context = super(HomeDetail, self).get_context_data(**kwargs)
        listing = ListingModel.objects.get(id=self.kwargs['pk'])
        context['listing_form_with_instance'] = list(ListingForm(instance=listing))
        return context

# dashboard home create view
class HomeCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = ListingForm
    login_url = 'login_page'
    template_name = "dashboard/home/home.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        context = {}
        context["listing_form"] = listing_form = ListingForm(request.POST, request.FILES)

        if listing_form.is_valid():
            listing_form.save()
            messages.success(self.request, f"Successfully added a listing!")
            return redirect("dashboard_home_page")
        for field in listing_form:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return render(request, self.template_name, context)

# dashboard home create view
class HomeUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ListingModel
    form_class = ListingForm
    login_url = 'login_page'
    template_name = "dashboard/home/home.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get_success_url(self):
        messages.success(self.request, "Successfully updated listing!")
        return reverse_lazy('dashboard_home_detail_page', kwargs={'pk': self.kwargs['pk']})

# dashboard home delete view
class HomeDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ListingModel
    login_url = 'login_page'
    template_name = "dashboard/home/detail.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get_success_url(self):
        messages.success(self.request, f"Successfully deleted listing!")
        return reverse_lazy('dashboard_home_page')

# dashboard account detail view
class AccountDetail(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'login_page'
    template_name = "dashboard/account/account.html"
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

    def get(self, request):
        context = {}
        user = User.objects.get(id=self.request.user.id)
        context['update_admin_form_with_instance'] = list(UpdateAdminForm(instance=user))
        context['update_user_form_with_instance'] = list(UpdateUserForm(instance=user))
        return render(request, self.template_name, context)

    def post(self, request):
        if request.user.is_admin:
            update_admin_form = UpdateAdminForm(request.POST, request.FILES, instance=request.user)
            if update_admin_form.is_valid():
                new_update_admin_form = update_admin_form.save(commit=False)
                new_update_admin_form.avatar = update_admin_form.cleaned_data.get('avatar')
                new_update_admin_form.first_name = update_admin_form.cleaned_data.get('first_name')
                new_update_admin_form.last_name = update_admin_form.cleaned_data.get('last_name')
                new_update_admin_form.email = update_admin_form.cleaned_data.get('email')
                new_update_admin_form.is_active = update_admin_form.cleaned_data.get('is_active')
                new_update_admin_form.staff = update_admin_form.cleaned_data.get('staff')
                new_update_admin_form.admin = update_admin_form.cleaned_data.get('admin')
                new_update_admin_form.save()
                messages.success(self.request, "Successfully updated account!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))
        elif request.user.instructormodel:
            update_user_form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
            if update_user_form.is_valid():
                new_update_user_form = update_user_form.save(commit=False)
                new_update_user_form.avatar = update_user_form.cleaned_data.get('avatar')
                new_update_user_form.first_name = update_user_form.cleaned_data.get('first_name')
                new_update_user_form.last_name = update_user_form.cleaned_data.get('last_name')
                new_update_user_form.email = update_user_form.cleaned_data.get('email')
                new_update_user_form.save()
                messages.success(self.request, "Successfully updated account!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))

# dashboard account delete view
class AccountDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    login_url = 'login_page'
    template_name = "dashboard/account/detail.html"
    raise_exception = True

    def test_func(self):
        return (not self.request.user.is_admin)

    def get_success_url(self):
        messages.success(self.request, f"Successfully deleted account!")
        return reverse_lazy('logout_page')

# account change password view
class AccountChangePassword(View):
    login_url = 'login_page'
    template_name = "dashboard/account/account.html"
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

    def get(self, request):
        context = {}
        context["change_password_form"] = PasswordChangeForm(request.user)
        return render(request, self.template_name, context)

    def post(self, request):
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))
        for field in password_change_form:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return render(request, self.template_name)

# order view
class Order(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "dashboard/order.html"
    login_url = 'login_page'
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get(self, request):
        FreeTrialOfferModel.objects.filter(created_on__lte=datetime.now(timezone.utc)-timezone.timedelta(days=7)).update(is_active=False)
        return render(request, self.template_name)




# student dashboard
class StudentDashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "dashboard/full_student_dashboard/dashboard.html"
    login_url = 'login_page'
    raise_exception = True

    def test_func(self):
        return (self.request.user.studentmodel)

    def get(self, request):
        context = {}
        labels = []
        data = []

        FreeTrialOfferModel.objects.filter(created_on__lte=datetime.now(timezone.utc)-timezone.timedelta(days=7)).update(is_active=False)

        programs = ProgramModel.objects.order_by("-id")
        for program in programs:
            labels.append(program.title)
            data.append(program.total_space)

        context["labels"] = labels
        context["data"] = data
        context["wallet"] = WalletModel.objects.get(user=request.user)
        return render(request, self.template_name, context)
 
# student account detail view
class StudentAccountDetail(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = 'login_page'
    template_name = "dashboard/full_student_dashboard/account.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.studentmodel)

    def get(self, request):
        context = {}
        user = User.objects.get(id=self.request.user.id)
        student = StudentModel.objects.get(user=user)
        context['student_form_with_instance'] = list(StudentForm(instance=student))
        context['update_user_form_with_instance'] = list(UpdateUserForm(instance=user))
        return render(request, self.template_name, context)

    def post(self, request):
        if request.user.studentmodel:
            student = StudentModel.objects.get(user=request.user)
            student_form = StudentForm(request.POST, instance=student)
            update_user_form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
            if update_user_form.is_valid() and student_form.is_valid():
                new_student_form = student_form.save(commit=False)
                new_update_user_form = update_user_form.save(commit=False)

                new_student_form.address = student_form.cleaned_data.get('address')
                new_student_form.dob = student_form.cleaned_data.get('dob')

                new_update_user_form.email = update_user_form.cleaned_data.get('email')
                new_update_user_form.avatar = update_user_form.cleaned_data.get('avatar')
                new_update_user_form.first_name = update_user_form.cleaned_data.get('first_name')
                new_update_user_form.last_name = update_user_form.cleaned_data.get('last_name')
                new_update_user_form.email = update_user_form.cleaned_data.get('email')

                new_student_form.save()
                new_update_user_form.save()
                messages.success(self.request, "Successfully updated account!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))

# student account change password view
class StudentAccountChangePassword(View):
    login_url = 'login_page'
    template_name = "dashboard/full_student_dashboard/account.html"
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

    def get(self, request):
        context = {}
        context["change_password_form"] = PasswordChangeForm(request.user)
        return render(request, self.template_name, context)

    def post(self, request):
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))
        for field in password_change_form:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return render(request, self.template_name)

# student package view
class StudentPackage(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = PackageModel
    login_url = 'login_page'
    template_name = "dashboard/full_student_dashboard/package.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.studentmodel)

    def get(self, request):
        context = {}
        context["wallet"] = WalletModel.objects.get(user=request.user)
        return render(request, self.template_name, context)

# get student package view
class GetStudentPackage(LoginRequiredMixin, UserPassesTestMixin, View):
    model = PackageModel
    login_url = 'login_page'
    raise_exception = True

    def test_func(self):
        return (self.request.user.studentmodel)

    def post(self, request, *args, **kwargs):
        package_id = self.kwargs['package_id']
        package_type = self.kwargs['package_type']
        package = PackageModel.objects.get(id=package_id)
        wallet = WalletModel.objects.get(user=request.user)

        if package_type == "bonus":
            for program in package.program.all():
                if program.total_space <= 0:
                    messages.error(self.request, "All space taken for some classes!")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            # checking wallet balance
            if wallet.balance < package.initial_price:
                messages.error(self.request, "Insufficient wallet balance! Please top-up your wallet")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            # update price
            new_wallet_balance = wallet.balance - package.initial_price
            wallet_balance = new_wallet_balance + package.bonus_price

            # updating wallet
            wallet.balance = wallet_balance
            wallet.save()

            # create order
            if request.user.ordermodel_set.filter(package=package).exists():
                # update price
                new_wallet_balance = wallet.balance + package.initial_price
                wallet_balance = new_wallet_balance - package.bonus_price

                # updating wallet
                wallet.balance = wallet_balance
                wallet.save()
                messages.error(self.request, f"This package is currently active on your account!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            order = OrderModel.objects.create(
                user = request.user,
                amount = package.initial_price,
                status = True,
                sessions = package.sessions,
            )
            order.package.add(package)
            order.program.add(*package.program.all())

            # adding student to instructors
            student = StudentModel.objects.get(user=request.user)
            program.students.add(student)

            # update program total space
            # program.total_space = program.total_space - 1
            program.save()

            messages.success(self.request, f"Successfully purchased package!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
        elif package_type == "kids":
            for program in package.program.all():
                if program.total_space <= 0:
                    messages.error(self.request, "All space taken for some classes!")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            new_wallet_balance = wallet.balance - package.initial_price

            if wallet.balance < package.initial_price:
                messages.error(self.request, "Insufficient wallet balance! Please top-up your wallet")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
            wallet.balance = new_wallet_balance
            wallet.save()

            # create order
            if request.user.ordermodel_set.filter(package=package).exists():
                # update price
                new_wallet_balance = wallet.balance + package.initial_price
                
                # updating wallet
                wallet.balance = new_wallet_balance
                wallet.save()

                messages.error(self.request, "This package is currently active on your account!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            order = OrderModel.objects.create(
                user = request.user,
                amount = package.initial_price,
                status = True,
                sessions = package.sessions,
                kids_sessions = package.kids_sessions,
            )
            order.package.add(package)
            order.program.add(*package.program.all())

            # adding student to instructors
            student = StudentModel.objects.get(user=request.user)
            program.students.add(student)

            # update program total space
            # program.total_space = program.total_space - 1
            program.save()

            messages.success(self.request, "Successfully purchased package with kids free session!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        elif package_type == "old":
            for program in package.program.all():
                if program.total_space <= 0:
                    messages.error(self.request, "All space taken for some classes!")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            new_wallet_balance = wallet.balance - package.initial_price

            if wallet.balance < package.initial_price:
                messages.error(self.request, "Insufficient wallet balance! Please top-up your wallet")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
            wallet.balance = new_wallet_balance
            wallet.save()

            # create order
            if request.user.ordermodel_set.filter(package=package).exists():
                # update price
                new_wallet_balance = wallet.balance + package.initial_price
                
                # updating wallet
                wallet.balance = new_wallet_balance
                wallet.save()

                messages.error(self.request, "This package is currently active on your account!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                
            order = OrderModel.objects.create(
                user = request.user,
                amount = package.initial_price,
                status = True,
                sessions = package.sessions,
                senior_citizen_sessions = package.senior_citizen_sessions,
            )
            order.package.add(package)
            order.program.add(*package.program.all())

            # adding student to instructors
            student = StudentModel.objects.get(user=request.user)
            program.students.add(student)

            # update program total space
            # program.total_space = program.total_space - 1
            program.save()

            messages.success(self.request, "Successfully purchased package with senior citizen free session!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# get ticket view
class GetTicket(View):
    login_url = 'login_page'
    raise_exception = True
    template = "dashboard/ticket.html"

    def get(self, request, *args, **kwargs):
        order_id = self.kwargs['order_id']
        
        try:
            order = OrderModel.objects.get(id=order_id)
        except:
            messages.error(self.request, f"This order does not longer exist!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        ticket = TicketModel.objects.filter(order=order).latest('id')

        context = {}
        context["ticket"] = ticket
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs['order_id']
        ticket_type = self.kwargs['ticket_type']
        
        try:
            order = OrderModel.objects.get(id=order_id)
        except:
            messages.error(self.request, f"This order does not longer exist!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        ticket = TicketModel.objects.create(order=order)
        
        if ticket_type == "sessions":
            context = {}
            email_cxt = {}
            context["ticket"] = ticket
            if order.sessions > 0:
                order.sessions = order.sessions - 1
                ticket.ticket_id = uuid.uuid1().hex[:10]
                order.save()
                ticket.save()
                if order.sessions == 0:
                    order.delete()
                
                # sending ticket through email
                current_site = get_current_site(request)
                email_cxt['ticket'] = True
                email_cxt['order_id'] = order.id
                email_cxt['ticket_type'] = ticket_type
                email_cxt['subject'] = subject = 'Naurs Entry Ticket.'
                to_email = order.user.email
                email_cxt['domain'] = current_site.domain
                email_cxt['message'] = f"""
                                            Hi {order.user.get_full_name()}, \n
                                            The Entry ticket link below: \n

                                        """
                actual_message = loader.render_to_string('components/notifications/emails.html', email_cxt)

                try:
                    send_mail(subject, actual_message, EMAIL_HOST_USER, [to_email], fail_silently = False, html_message=actual_message)
                    messages.success(self.request, f"Check email inbox or spam for link to this ticket. <br> You have {order.sessions} session(s) remaining!")
                    return render(request, self.template, context)
                except socket.gaierror:
                    messages.error(request, 'No internet connect')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                except HeaderParseError:
                    messages.error(request, 'A user has an invalid domain')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                except BadHeaderError:
                    messages.error(request, 'Bad header')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                except TimeoutError:
                    messages.error(request, 'Time out')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                except ValueError as e:
                    messages.error(request, f'{e}')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            messages.error(self.request, f"You have no sessions!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if ticket_type == "kids_sessions":
            context = {}
            email_cxt = {}
            context["ticket"] = ticket
            if order.kids_sessions > 0:
                order.kids_sessions = order.kids_sessions - 1
                ticket.ticket_id = uuid.uuid1().hex[:10]
                order.save()
                ticket.save()

                # sending ticket through email
                current_site = get_current_site(request)
                email_cxt['ticket'] = True
                email_cxt['order_id'] = order.id
                email_cxt['ticket_type'] = ticket_type
                email_cxt['subject'] = subject = 'Naurs Entry Ticket.'
                to_email = order.user.email
                email_cxt['domain'] = current_site.domain
                email_cxt['message'] = f"""
                                            Hi {order.user.get_full_name()}, \n
                                            The Entry ticket link below: \n

                                        """
                actual_message = loader.render_to_string('components/notifications/emails.html', email_cxt)

                try:
                    send_mail(subject, actual_message, EMAIL_HOST_USER, [to_email], fail_silently = False, html_message=actual_message)
                    messages.success(self.request, f"Check email inbox or spam for link to this ticket. <br> You have {order.kids_sessions} kids session(s) remaining!")
                    return render(request, self.template, context)
                except socket.gaierror:
                    messages.error(request, 'No internet connect')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                except HeaderParseError:
                    messages.error(request, 'A user has an invalid domain')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                except BadHeaderError:
                    messages.error(request, 'Bad header')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                except TimeoutError:
                    messages.error(request, 'Time out')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                except ValueError as e:
                    messages.error(request, f'{e}')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            messages.error(self.request, f"You have no free kids sessions!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if ticket_type == "senior_citizen_sessions":
            context = {}
            email_cxt = {}
            context["ticket"] = ticket
            if order.senior_citizen_sessions > 0:
                order.senior_citizen_sessions = order.senior_citizen_sessions - 1
                ticket.ticket_id = uuid.uuid1().hex[:10]
                order.save()
                ticket.save()

                # sending ticket through email
                current_site = get_current_site(request)
                email_cxt['ticket'] = True
                email_cxt['order_id'] = order.id
                email_cxt['ticket_type'] = ticket_type
                email_cxt['subject'] = subject = 'Naurs Entry Ticket.'
                to_email = order.user.email
                email_cxt['domain'] = current_site.domain
                email_cxt['message'] = f"""
                                            Hi {order.user.get_full_name()}, \n
                                            The Entry ticket link below: \n

                                        """
                actual_message = loader.render_to_string('components/notifications/emails.html', email_cxt)

                try:
                    send_mail(subject, actual_message, EMAIL_HOST_USER, [to_email], fail_silently = False, html_message=actual_message)
                    messages.success(self.request, f"Check email inbox or spam for link to this ticket. <br> You have {order.senior_citizen_sessions} senior citizen session(s) remaining!")
                    return render(request, self.template, context)
                except socket.gaierror:
                    messages.error(request, 'No internet connect')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                except HeaderParseError:
                    messages.error(request, 'A user has an invalid domain')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                except BadHeaderError:
                    messages.error(request, 'Bad header')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                except TimeoutError:
                    messages.error(request, 'Time out')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                except ValueError as e:
                    messages.error(request, f'{e}')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            messages.error(self.request, f"You have no free senior citizen sessions!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# student calendar view
class StudentCalendar(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = PackageModel
    login_url = 'login_page'
    template_name = "dashboard/full_student_dashboard/calendar.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.studentmodel)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month, self.request.user)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context        

# get instructor notification view
class InstructorNotification(LoginRequiredMixin, UserPassesTestMixin, View):
    model = InstructorNotificationModel
    login_url = 'login_page'
    raise_exception = True
    template_name = "dashboard/instructor/notification.html"

    def test_func(self):
        return (self.request.user.instructormodel)

    def get(self, request, *args, **kwargs):
        context = {}
        instructor = InstructorModel.objects.get(user=self.request.user)
        context['instructor_notifications'] = InstructorNotificationModel.objects.filter(instructor=instructor).order_by("-id")
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        context["instructor_notification_form"] = notification_form = InstructorNotificationForm(request.POST)

        if notification_form.is_valid():
            notification_form = notification_form.save(commit=False)
            instructor = InstructorModel.objects.get(user=self.request.user)
            notification_form.instructor = instructor
            notification_form.save()
            messages.success(self.request, "Successfully sent message!")
            return redirect("dashboard_instructor_notification_page")
        for field in notification_form:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return redirect("dashboard_instructor_notification_page")

# get instructor notification update view
class InstructorNotificationUpdate(LoginRequiredMixin, UserPassesTestMixin, View):
    model = InstructorNotificationModel
    login_url = 'login_page'
    raise_exception = True
    template_name = "dashboard/instructor/notification.html"

    def test_func(self):
        return (self.request.user.instructormodel)

    def get(self, request, *args, **kwargs):
        notification = InstructorNotificationModel.objects.get(id=self.kwargs['id'])
        if self.kwargs['type'] == "read" and self.kwargs['user'] == "instructor":
            notification.instructor_read = True
            notification.save()
        elif self.kwargs['type'] == "unread" and self.kwargs['user'] == "instructor":
            notification.instructor_read = False
            notification.save()
        elif self.kwargs['type'] == "read" and self.kwargs['user'] == "student":
            notification.student_read = True
            notification.save()
        elif self.kwargs['type'] == "unread" and self.kwargs['user'] == "student":
            notification.student_read = False
            notification.save()
        messages.success(self.request, "Notification updated!")
        return redirect("dashboard_instructor_notification_page")

class Tickets(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = TicketModel
    login_url = 'login_page'
    template_name = "dashboard/admin/tickets.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get(self, request):
        context = {}
        context["tickets"] = TicketModel.objects.order_by("-id")
        return render(request, self.template_name, context)

class TicketRevert(LoginRequiredMixin, UserPassesTestMixin, View):
    model = TicketModel
    login_url = 'login_page'
    template_name = "dashboard/admin/tickets.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def post(self, request, *args, **kwargs):
        ticket = TicketModel.objects.get(id=self.kwargs['pk'])
        wallet = WalletModel.objects.get(user=ticket.order.user)
        new_balance = wallet.balance + ticket.order.amount
        wallet.balance = new_balance
        wallet.save()

        if ticket.order.sessions > 0:
            new_session = ticket.order.sessions + 1
            ticket.order.sessions = new_session
            ticket.order.save()

        for program in ticket.order.program.all():
            new_total_space = program.total_space + 1
            program.total_space = new_total_space
            program.save()

        ticket.delete()
        messages.success(self.request, "Successfully reverted ticket!")
        return redirect('dashboard_tickets_page')

class TicketDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TicketModel
    login_url = 'login_page'
    template_name = "dashboard/admin/tickets.html"
    raise_exception = True

    def test_func(self):
        return (self.request.user.is_admin)

    def get_success_url(self):
        messages.success(self.request, "Successfully deleted ticket!")
        return reverse_lazy('dashboard_tickets_page')

# get notification view
class Notification(LoginRequiredMixin, UserPassesTestMixin, View):
    model = NotificationModel
    login_url = 'login_page'
    raise_exception = True
    template_name = "dashboard/admin/notification.html"

    def test_func(self):
        return (self.request.user.is_admin)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        context = {}
        context["notification_form"] = notification_form = NotificationForm(request.POST)

        if notification_form.is_valid():
            notification_form.save()
            messages.success(self.request, "Successfully sent message!")
            return redirect("dashboard_notification_page")
        for field in notification_form:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return redirect("dashboard_notification_page")

