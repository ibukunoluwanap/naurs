from django.contrib import messages
from django.views.generic import View
from account.forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http.response import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate

# setting User model
User = get_user_model()

# register view
class Register(View):
    template_name = "account/register.html"
    form = RegisterForm()

    def get(self, request):
        context = {}
        # checking if user is logged in
        if request.user.is_authenticated:
            messages.info(request, 'You are logged in already! Please download the mobile app on your device to access our programs')
            return redirect('home_page')
        context["form"] = self.form
        return render(request, self.template_name, context)

    def post(self,request):
        context = {}
        form = RegisterForm(request.POST)
        context["form"] = form

        if form.is_valid():
            # getting email data from form
            email = form.cleaned_data.get('email')

            # validating email address in database
            if User.objects.filter(email=email).exists():
                messages.success(request, 'Email already exist!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            # saving user to database
            user = form.save()
            # login the user
            login(request, user)
            messages.success(request, "Successfully registered and logged in!")
            return redirect('home_page')
        return render(request, self.template_name, context)

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

# logout class
class Logout(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        logout(request)
        messages.success(request, 'Successfully logged out!')
        return redirect('home_page')