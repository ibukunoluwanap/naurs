from django.contrib import messages
from program.forms import ProgramEnquiryForm
from .models import PackageModel, ProgramEnquiryModel, ProgramModel
from django.shortcuts import redirect
from django.views.generic import FormView, ListView, DetailView

# program music view
class ProgramMusic(ListView):
    model = ProgramModel
    template_name = "program/music.html"

# program fitness view
class ProgramFitness(ListView):
    model = ProgramModel
    template_name = "program/fitness.html"

# program fine arts view
class ProgramFineArts(ListView):
    model = ProgramModel
    template_name = "program/fine_arts.html"

# program dance view
class ProgramDance(ListView):
    model = ProgramModel
    template_name = "program/dance.html"

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

# package view
class Package(ListView):
    model = PackageModel
    template_name = "package/package.html"

# package detail view
class PackageDetail(DetailView):
    model = PackageModel
    template_name = "package/detail.html"
    context_object_name = "package"