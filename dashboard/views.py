from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from about.forms import AboutForm
from about.models import AboutModel
from account.forms import UpdateAdminForm, UpdateUserForm
from home.forms import ListingForm
from home.models import ListingModel
from instructor.forms import InstructorForm
from instructor.models import InstructorModel
from offer.forms import OfferForm
from django.contrib import messages
from offer.models import BookOfferModel, OfferModel
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from program.forms import PackageForm, ProgramBenefitForm, ProgramForm
from program.models import PackageModel, ProgramBenefitModel, ProgramEnquiryModel, ProgramModel
from django.contrib.auth import get_user_model
from student.forms import StudentForm
from django.contrib.auth.mixins import UserPassesTestMixin
from student.models import StudentModel
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

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

        programs = ProgramModel.objects.order_by("-id")
        for program in programs:
            labels.append(program.title)
            data.append(program.total_space)

        context["labels"] = labels
        context["data"] = data
        return render(request, self.template_name, context)

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
            messages.success(self.request, f"Successfully created a program!")
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
    raise_exception = True

    def test_func(self):
        try:
            return (self.request.user.instructormodel)
        except:
            return (self.request.user.is_admin)

    def get_success_url(self):
        messages.success(self.request, "Successfully updated program!")
        return reverse_lazy('dashboard_program_detail_page', kwargs={'pk': self.kwargs['pk']})

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
                messages.success(self.request, "Successfully deactivated program!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))
            program.is_active = True
            program.save()
            messages.success(self.request, "Successfully reactivated program!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/dashboard/'))
        elif visibility == 'delete':
            program.delete()
            messages.success(self.request, "Successfully deleted program!")
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
        context['program_form_with_instance'] = list(PackageForm(instance=package))
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

# dashboard offer view
class Offer(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = OfferModel
    login_url = 'login_page'
    template_name = "dashboard/offer/offer.html"
    raise_exception = True

    def test_func(self):
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

        if instructor_form.is_valid():
            user = instructor_form.cleaned_data.get('user')
            if user.is_admin:
                messages.error(self.request, f"{user} is admin and cannot be instructor!")
                return redirect("dashboard_instructor_page")
            else:
                try:
                    if user.studentmodel:
                        messages.error(self.request, f"{user} is student and cannot be instructor!")
                        return redirect("dashboard_instructor_page")
                    elif user.instructormodel:
                        messages.info(self.request, f"{user} already a instructor!")
                        return redirect("dashboard_instructor_page")
                except:
                    instructor_form.save()
                    messages.success(self.request, f"Successfully added an instructor!")
                    return redirect("dashboard_instructor_page")
        for field in instructor_form:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return render(request, self.template_name, context)

# dashboard instructor create view
class InstructorUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = InstructorModel
    form_class = InstructorForm
    login_url = 'login_page'
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
        messages.success(self.request, f"Successfully deleted about!")
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
        return render(request, self.template_name, context)

    def post(self, request):
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
