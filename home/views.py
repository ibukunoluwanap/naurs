import calendar
from django.shortcuts import render
from django.views.generic import ListView, View
from home.models import CalendarModel, ListingModel
from home.utils import Calendar
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta, date

# home list view
class Home(ListView):
    model = ListingModel
    login_url = 'login_page'
    template_name = "home/home.html"

# calendar view
class CalendarView(ListView):
    model = CalendarModel
    template_name = 'home/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class PrivacyPolicyView(View):
    template_name = "home/privacy_policy.html"

    def get(self, *arg, **kwargs):
        return render(self.request, self.template_name)

