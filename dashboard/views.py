from django.views.generic import View
from django.shortcuts import render

# dashboard list view
class Dashboard(View):
    template_name = "dashboard/dashboard.html"
    def get(self, request):
        return render(request, self.template_name)
