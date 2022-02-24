from django.contrib import messages
from program.forms import ProgramEnquiryForm
from .models import ProgramEnquiryModel, ProgramModel
from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView, DetailView

# program view
class Program(ListView):
    model = ProgramModel
    template_name = "program/program.html"

# program detail view
class ProgramDetail(DetailView):
    model = ProgramModel
    template_name = "program/detail.html"
    context_object_name = "program"

# program enquiry view
class ProgramEnquiry(FormView):
    template_name = "program/detail.html"
    model = ProgramEnquiryModel
    form_class = ProgramEnquiryForm

    def form_valid(self, form):
        program = ProgramModel.objects.get(id=self.kwargs['program_id'])
        program_enquiry = form.save(False)
        program_enquiry.program = program
        program_enquiry.save()
        messages.success(self.request, f"{program_enquiry.name} successfully submitted enquiry!")
        return redirect("program_detail_page", pk=self.kwargs['program_id'])