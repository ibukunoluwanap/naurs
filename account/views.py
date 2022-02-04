from django.views.generic import View
from django.shortcuts import render

# register view
class Register(View):
    template_name = "account/register.html"
    def get(self, request):
        return render(request, self.template_name)

# login view
class Login(View):
    template_name = "account/login.html"
    def get(self, request):
        return render(request, self.template_name)

# forgot view
class ForgetPassword(View):
    template_name = "account/forget_password.html"
    def get(self, request):
        return render(request, self.template_name)
