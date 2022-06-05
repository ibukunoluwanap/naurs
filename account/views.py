from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import messages
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from account.forms import RegisterForm, LoginForm
from django.http.response import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from finance.models import WalletModel
from naurs.settings import EMAIL_HOST_USER
from offer.models import FreeTrialOfferModel
from student.models import StudentModel
from django.core.mail import send_mail, BadHeaderError
from django.utils import timezone
from datetime import datetime
import six, socket
from email.errors import HeaderParseError
from django.template import loader

# setting User model
User = get_user_model()

# email token
class EmailVerificationToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        token = six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        return token
        
# email verification
class VerifyEmail(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            user = None
            messages.error(request, 'Invalid user ID')
            return redirect('main')
            
        if user is not None and EmailVerificationToken().check_token(user, token):
            user.is_active = True
            user.save()

            # login the user
            FreeTrialOfferModel.objects.filter(created_on__lte=datetime.now(timezone.utc)-timezone.timedelta(days=7)).update(is_active=False)
            
            student = StudentModel.objects.create(user=user)
            if student:
                WalletModel.objects.create(user=user)
                messages.success(request, 'Thank you for your email confirmation. Now you can login.')
                return redirect('login_page')
        messages.error(request, 'Activation link is invalid!')
        return redirect('login_page')

# register view
class Register(View):
    template_name = "account/register.html"

    def get(self, request):
        # checking if user is logged in
        if request.user.is_authenticated:
            messages.info(request, 'You are logged in! Please download the mobile app on your device to access our classes & packages')
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
                messages.success(request, 'User with this email address already exists!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            #  disable new user
            user = register_form.save(commit=False)
            user.is_active = False # disable user
            user.save()

            # send verification email
            current_site = get_current_site(request)
            context['subject'] = subject = 'Naurs Email Activation.'
            to_email = email
            context['domain'] = current_site.domain
            context['uid'] = urlsafe_base64_encode(force_bytes(user.pk))
            context['token'] = EmailVerificationToken().make_token(user)
            context['message'] = f"Hi {email}, Please verify your Naurs account to be able to login by clicking on the link below to confirm your registration."
            actual_message = loader.render_to_string('components/notifications/emails.html', context)

            try:
                send_mail(subject, actual_message, EMAIL_HOST_USER, [to_email], fail_silently = False, html_message=actual_message)
                messages.success(request, 'Check email inbox or spam to confirm email!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except socket.gaierror:
                messages.error(request, 'No internet connect')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except HeaderParseError:
                messages.error(request, 'A user has an invalid domain')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except BadHeaderError:
                messages.error(request, 'Bad header')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except TimeoutError:
                messages.error(request, 'Time out')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except ValueError as e:
                messages.error(request, f'{e}')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        for field in register_form:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
        return render(request, self.template_name, context)

# login view
class Login(View):
    template_name = "account/login.html"

    def get(self, request):
        # checking if user is logged in
        if request.user.is_authenticated:
            messages.info(request, 'You are logged in! Please download the mobile app on your device to access our classes & packages')
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
                    FreeTrialOfferModel.objects.filter(created_on__lte=datetime.now(timezone.utc)-timezone.timedelta(days=7)).update(is_active=False)
                    messages.success(request, f"Welcome { user }!")
                    return redirect('dashboard_page')
                try:
                    if user.instructormodel:
                        login(request, user)
                        FreeTrialOfferModel.objects.filter(created_on__lte=datetime.now(timezone.utc)-timezone.timedelta(days=7)).update(is_active=False)
                        messages.success(request, f"Welcome { user.instructormodel }!")
                        return redirect('dashboard_page')
                except:
                    try:
                        if user.studentmodel:
                            messages.info(request, 'You are logged in! Please download the mobile app on your device to access our classes & packages')
                            return redirect('login_page')
                            # login(request, user)
                            # FreeTrialOfferModel.objects.filter(created_on__lte=datetime.now(timezone.utc)-timezone.timedelta(days=7)).update(is_active=False)
                            # messages.success(request, "Successfully registered select package to start with!")
                            # return redirect('student_dashboard_page')
                    except:
                        pass
            messages.error(request, "Check user's credentials OR Verify your email!")
            return redirect('login_page')

        for field in login_form:
            for error in field.errors:
                messages.error(self.request, f"<b>{field.label}:</b> {error}")
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
        FreeTrialOfferModel.objects.filter(created_on__lte=datetime.now(timezone.utc)-timezone.timedelta(days=7)).update(is_active=False)
        logout(request)
        messages.success(request, 'Successfully logged out!')
        return redirect('login_page')