from django.contrib import messages
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from account.forms import RegisterForm, LoginForm
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

    def post(self, request):
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
    form = LoginForm()

    def get(self, request):
        context = {}
        # checking if user is logged in
        if request.user.is_authenticated:
            messages.info(request, 'You are logged in already! Please download the mobile app on your device to access our programs')
            return redirect('home_page')
        context["form"] = self.form
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        form = LoginForm(request.POST)
        context["form"] = form

        if form.is_valid():
            # getting email data from form
            email = request.POST['email']
            password = request.POST['password']

            # authenticating user
            user = authenticate(email=email, password=password)

            print(email, password, user)

            # login the user
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome { request.user.username }!")
                return redirect('home_page')
            messages.error(request, "Check user's credentials!") 
            return redirect('login_page')
        return render(request, self.template_name, context)

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