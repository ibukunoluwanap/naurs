from django.shortcuts import redirect, render
from about.forms import AboutForm
from about.models import AboutModel
from account.forms import UpdateAdminForm, UpdateUserForm
from home.forms import ListingForm
from home.models import ListingModel
from instructor.forms import InstructorForm
from instructor.models import InstructorModel
from offer.forms import OfferForm
from django.contrib import messages
from offer.models import OfferModel
from django.views.generic import View, ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from program.forms import ProgramBenefitInlineFormset, ProgramForm
from program.models import ProgramModel
from django.urls import reverse
from django.contrib.auth import get_user_model

# setting User model
User = get_user_model()

# dashboard list view
class Dashboard(LoginRequiredMixin, View):
    template_name = "dashboard/dashboard.html"
    login_url = 'login_page'

    def get(self, request):
        context = {}
        labels = []
        data = []

        programs = ProgramModel.objects.order_by("-id")
        for program in programs:
            labels.append(program.title)
            data.append(program.total_space)

            print(labels, data)
        
        context["labels"] = labels
        context["data"] = data
        return render(request, self.template_name, context)

# dashboard program view
class Program(LoginRequiredMixin, ListView):
    model = ProgramModel
    login_url = 'login_page'
    template_name = "dashboard/program/program.html"

# dashboard program detail view
class ProgramDetail(LoginRequiredMixin, DetailView):
    model = ProgramModel
    login_url = 'login_page'
    template_name = "dashboard/program/detail.html"
    context_object_name = "program"

    def get_context_data(self, **kwargs):
        context = super(ProgramDetail, self).get_context_data(**kwargs)
        program = ProgramModel.objects.get(id=self.kwargs['pk'])
        context['program_form_with_instance'] = list(ProgramForm(instance=program))
        context['program_benefit_inline_formset_with_instance'] = list(ProgramBenefitInlineFormset(instance=program))
        return context

# dashboard program create view
class ProgramCreate(LoginRequiredMixin, CreateView):
    form_class = ProgramForm
    login_url = 'login_page'
    template_name = "dashboard/program/detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProgramCreate, self).get_context_data(**kwargs)
        context['program_benefit_inline_formset'] = ProgramBenefitInlineFormset()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        program_benefit_inline_formset = ProgramBenefitInlineFormset(self.request.POST)
        if form.is_valid() and program_benefit_inline_formset.is_valid():
            return self.form_valid(form, program_benefit_inline_formset)
        else:
            return self.form_invalid(form, program_benefit_inline_formset)

    def form_valid(self, form, program_benefit_inline_formset):
        self.object = form.save(commit=False)
        self.object.save()
        # saving program benefit instances
        program_benefit = program_benefit_inline_formset.save(commit=False)
        for benefit in program_benefit:
            benefit.program = self.object
            benefit.save()
        return redirect(reverse("program:dashboard_program_page"))

    def form_invalid(self, form, program_benefit_inline_formset):
        return self.render_to_response(self.get_context_data(form, program_benefit_inline_formset))

# dashboard offer view
class Offer(LoginRequiredMixin, ListView):
    model = OfferModel
    login_url = 'login_page'
    template_name = "dashboard/offer/offer.html"

# dashboard offer detail view
class OfferDetail(LoginRequiredMixin, DetailView):
    model = OfferModel
    login_url = 'login_page'
    template_name = "dashboard/offer/detail.html"
    context_object_name = "offer"

    def get_context_data(self, **kwargs):
        context = super(OfferDetail, self).get_context_data(**kwargs)
        offer = OfferModel.objects.get(id=self.kwargs['pk'])
        context['offer_form_with_instance'] = list(OfferForm(instance=offer))
        return context

# dashboard offer create view
class OfferCreate(LoginRequiredMixin, CreateView):
    model = OfferModel
    form_class = OfferForm
    template_name = "dashboard/offer/create.html"
    login_url = 'login_page'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        context = {}
        context["offer_form"] = offer_form = OfferForm(request.POST, request.FILES)

        if offer_form.is_valid():
            offer_form.save()
            messages.success(self.request, f"Successfully created an offer!")
            return redirect("dashboard_offer_create_page")
        return render(request, self.template_name, context)

# dashboard instructor view
class Instructor(LoginRequiredMixin, ListView):
    model = InstructorModel
    login_url = 'login_page'
    template_name = "dashboard/instructor/instructor.html"

# dashboard instructor detail view
class InstructorDetail(LoginRequiredMixin, DetailView):
    model = InstructorModel
    login_url = 'login_page'
    template_name = "dashboard/instructor/detail.html"
    context_object_name = "instructor"

    def get_context_data(self, **kwargs):
        context = super(InstructorDetail, self).get_context_data(**kwargs)
        instructor = InstructorModel.objects.get(id=self.kwargs['pk'])
        context['instructor_form_with_instance'] = list(InstructorForm(instance=instructor))
        context['update_user_form_with_instance'] = UpdateUserForm(instance=instructor.user)
        return context

# dashboard admin view
class Admin(LoginRequiredMixin, ListView):
    model = User
    login_url = 'login_page'
    template_name = "dashboard/admin/admin.html"

# dashboard admin detail view
class AdminDetail(LoginRequiredMixin, DetailView):
    model = User
    login_url = 'login_page'
    template_name = "dashboard/admin/detail.html"
    context_object_name = "admin"

    def get_context_data(self, **kwargs):
        context = super(AdminDetail, self).get_context_data(**kwargs)
        admin = User.objects.get(id=self.kwargs['pk'], admin=True)
        context['admin_form_with_instance'] = list(UpdateAdminForm(instance=admin))
        return context


# dashboard about view
class About(LoginRequiredMixin, ListView):
    model = AboutModel
    login_url = 'login_page'
    template_name = "dashboard/about/about.html"

# dashboard about detail view
class AboutDetail(LoginRequiredMixin, DetailView):
    model = AboutModel
    login_url = 'login_page'
    template_name = "dashboard/about/detail.html"
    context_object_name = "about"

    def get_context_data(self, **kwargs):
        context = super(AboutDetail, self).get_context_data(**kwargs)
        about = AboutModel.objects.get(id=self.kwargs['pk'])
        context['about_form_with_instance'] = list(AboutForm(instance=about))
        return context

# dashboard home view
class Home(LoginRequiredMixin, ListView):
    model = ListingModel
    login_url = 'login_page'
    template_name = "dashboard/home/home.html"

# dashboard home detail view
class HomeDetail(LoginRequiredMixin, DetailView):
    model = ListingModel
    login_url = 'login_page'
    template_name = "dashboard/home/detail.html"
    context_object_name = "listing"

    def get_context_data(self, **kwargs):
        context = super(HomeDetail, self).get_context_data(**kwargs)
        listing = ListingModel.objects.get(id=self.kwargs['pk'])
        context['listing_form_with_instance'] = list(ListingForm(instance=listing))
        return context

# dashboard account detail view
class AccountDetail(LoginRequiredMixin, View):
    login_url = 'login_page'
    template_name = "dashboard/account/account.html"

    def get(self, request):
        context = {}
        user = User.objects.get(id=self.request.user.id)
        context['user_form_with_instance'] = list(UpdateAdminForm(instance=user))
        return render(request, self.template_name, context)
