from django.contrib import messages
from program.forms import ProgramEnquiryForm
from program.utils import Calendar
from .models import PackageModel, ProgramEnquiryModel, ProgramModel
from django.shortcuts import redirect
from django.views.generic import FormView, ListView, DetailView
from django.utils.safestring import mark_safe
from datetime import date, datetime

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

# package view
class Package(ListView):
    model = PackageModel
    template_name = "package/package.html"

# package detail view
class PackageDetail(DetailView):
    model = PackageModel
    template_name = "package/detail.html"
    context_object_name = "package"



class CalendarView(ListView):
    model = ProgramModel
    template_name = 'program/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()