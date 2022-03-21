from django.contrib import messages
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from account.forms import RegisterForm, LoginForm
from django.http.response import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate

# setting User model
User = get_user_model()

# register view
class Register(View):
    template_name = "account/register.html"

    def get(self, request):
        # checking if user is logged in
        if request.user.is_authenticated:
            messages.info(request, 'You are logged in already! Please download the mobile app on your device to access our programs')
            return redirect('home_page')
        return render(request, self.template_name)

    def post(self, request):
        context = {}
        context["register_form"] = register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            # getting email data from register form
            email = register_form.cleaned_data.get('email')

            # validating email address in database
            if User.objects.filter(email=email).exists():
                messages.success(request, 'Email already exist!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            # saving user to database
            user = register_form.save()
            # login the user
            login(request, user)
            messages.success(request, "Successfully registered and logged in! Select program & class to start with")
            return redirect('program_page')
        messages.error(self.request, f"{register_form.errors}")
        return render(request, self.template_name, context)

# login view
class Login(View):
    template_name = "account/login.html"

    def get(self, request):
        # checking if user is logged in
        if request.user.is_authenticated:
            messages.info(request, 'You are logged in already! Please download the mobile app on your device to access our programs')
            return redirect('login_page')
        return render(request, self.template_name)

    def post(self, request):
        context = {}
        context["login_form"] = login_form = LoginForm(request.POST)

        if login_form.is_valid():
            # getting email data from login form
            email = request.POST['email']
            password = request.POST['password']

            # authenticating user
            user = authenticate(email=email, password=password)

            # login the user
            if user is not None:
                if user.is_admin:
                    login(request, user)
                    messages.success(request, f"Welcome { user }!")
                    return redirect('dashboard_page')
                try:
                    if user.instructormodel:
                        login(request, user)
                        messages.success(request, f"Welcome { user.instructormodel }!")
                        return redirect('dashboard_page')
                except:
                    login(request, user)
                    messages.info(request, 'You are logged in! Please download the mobile app on your device to access our programs')
                    return redirect('home_page')
            messages.error(request, "Check user's credentials!")
            return redirect('login_page')
        messages.error(self.request, f"{login_form.errors}")
        return render(request, self.template_name, context)

# password reset done
class PasswordResetDone(View):
    def get(self, request):
        messages.success(
            request,
            """
                <p>
                    We've emailed you instructions for setting your password, only if an account exists with the email you entered.
                    You should receive them shortly.
                </p>
                <p>
                    If you don't receive an email, please make sure you've entered the address you registered with,
                    and check your spam folder.
                </p>
            """
            ) 
        return redirect("password_reset")

# password reset complete
class PasswordResetComplete(View):
    def get(self, request):
        messages.success(
            request,
            """
                <p>
                    Your password has been set. You may go ahead and <a href="{% url 'login_page' %}">sign in</a> now!
                </p>
            """
            ) 
        return redirect("home_page")

# logout class
class Logout(LoginRequiredMixin, View):
    login_url = 'login_page'

    def get(self, request):
        logout(request)
        messages.success(request, 'Successfully logged out!')
        return redirect('login_page')