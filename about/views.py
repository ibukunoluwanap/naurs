from django.views.generic import View
from django.shortcuts import render

# about list view
class About(View):
    template_name = "about/about.html"
    def get(self, request):
        return render(request, self.template_name)
