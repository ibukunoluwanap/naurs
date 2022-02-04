from django.contrib import messages
from django.views.generic import View
from account.forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

# register view
class Register(View):
    template_name = "account/register.html"
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self,request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            messages.success(request, "Successfully registered")
            return redirect('home_page')
        for error in form.errors:
            messages.error(request, error)
        return redirect('register_page')

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
