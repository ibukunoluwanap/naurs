from django.views.generic import View
from django.shortcuts import render

# register view
class Register(View):
    template_name = "account/register.html"
    def get(self, request):
        return render(request, self.template_name)
