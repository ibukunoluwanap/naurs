from django.shortcuts import redirect, render
from offer.forms import OfferForm
from django.contrib import messages
from offer.models import OfferModel
from django.views.generic import View, ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from program.forms import ProgramBenefitForm, ProgramBenefitInlineFormset, ProgramForm
from program.models import ProgramBenefitModel, ProgramModel
from django.urls import reverse

# dashboard list view
class Dashboard(LoginRequiredMixin, View):
    template_name = "dashboard/dashboard.html"
    login_url = 'login_page'

    def get(self, request):
        return render(request, self.template_name)

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
        context['program_benefit_inline_formset_with_instance'] = list(ProgramBenefitInlineFormset())
        return context

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
            return redirect("offer_create_page")
        return render(request, self.template_name, context)