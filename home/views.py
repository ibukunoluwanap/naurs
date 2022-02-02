from django.views.generic import View
from django.shortcuts import render

# home list view
class Home(View):
    template_name = "home/home.html"
    def get(self, request):
        return render(request, self.template_name)
