from venv import create
from django.shortcuts import render
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from account.serializers import ChangePasswordSerializer, LoginSerializer, UserSerializer, RegisterSerializer
from account.views import EmailVerificationToken
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from email.errors import HeaderParseError
from django.template import loader
from django.core.mail import send_mail, BadHeaderError
from api.custom import CustomAuthTokenSerializer
from finance.models import OrderModel
from finance.serializers import OrderSerializer
from home.models import CalendarModel
from home.serializers import CalendarSerializer
from naurs.settings import EMAIL_HOST_USER, DOMAIN
import socket
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from rest_framework import status
from django.views.generic import View
from program.models import PackageModel, ProgramModel
from program.serializers import PackageSerializer, ProgramSerializer
from django.utils import timezone

User = get_user_model()

# user API
class UserAPI(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

# register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        context = {}
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            for error in serializer.errors:
                response = {
                    'status': 'error',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': f"{serializer.errors[error][0]}"
                }
                return Response(response)

        user = serializer.save(is_active=False)

        # send verification email
        current_site = get_current_site(request)
        context['subject'] = subject = 'Naurs Email Activation.'
        to_email = user.email
        context['domain'] = current_site.domain
        context['uid'] = urlsafe_base64_encode(force_bytes(user.pk))
        context['token'] = EmailVerificationToken().make_token(user)
        context['message'] = f"Hi {user.email}, Please verify your Naurs account to be able to login by clicking on the link below to confirm your registration."
        actual_message = loader.render_to_string('components/notifications/emails.html', context)

        try:
            send_mail(subject, actual_message, EMAIL_HOST_USER, [to_email], fail_silently = False, html_message=actual_message)
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': "Check email inbox or spam to confirm email!"
            }
            return Response(response)
        except socket.gaierror:
            response = {
                'status': 'error',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': "No internet connect"
            }
            return Response(response)
        except HeaderParseError:
            response = {
                'status': 'error',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': "A user has an invalid domain"
            }
            return Response(response)
        except BadHeaderError:
            response = {
                'status': 'error',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': "Bad header"
            }
            return Response(response)
        except TimeoutError:
            response = {
                'status': 'error',
                'code': status.HTTP_408_REQUEST_TIMEOUT,
                'message': "Time out"
            }
            return Response(response)
        except ValueError as error:
            response = {
                'status': 'error',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': f"{error}"
            }
            return Response(response)

# login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = CustomAuthTokenSerializer(data=request.data)
        
        if not serializer.is_valid():
            for error in serializer.errors:
                response = {
                    'status': 'error',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': {
                        "user": {},
                        "token": f"{serializer.errors[error][0]}"
                    }
                    # 'message': {"message": f"{serializer.errors[error][0]}"}
                }
                return Response(response)

        user = serializer.validated_data['user']
        login(request, user)

        response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': {
                    "user": UserSerializer(user, context=self.get_serializer_context()).data,
                    "token": AuthToken.objects.create(user)[1]
                }
            }
        
        return Response(response)

# change password API
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    model = User

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            for error in serializer.errors:
                response = {
                    'status': 'error',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': f"{serializer.errors[error][0]}"
                }
                return Response(response)

        # Check old password
        if not self.object.check_password(serializer.data.get("old_password")):
            error_response = {
                'status': 'error',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Old password is wrong!'
            }

            return Response(error_response)

        # set_password also hashes the password that the user will get
        self.object.set_password(serializer.data.get("new_password"))
        self.object.save()

        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully!'
        }

        return Response(response)

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    context = {}
    context['subject'] = subject = 'Reset Password'
    to_email = reset_password_token.user.email
    context['domain'] = DOMAIN
    context['token'] = reset_password_token.key

    # email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    actual_message = loader.render_to_string('account/api/forgot_password_email.html', context)
    send_mail(subject, actual_message, EMAIL_HOST_USER, [to_email], fail_silently = False, html_message=actual_message)

class PasswordResetConfirm(View):
    template_name = "account/api/forgot_password_confirm.html"

    def get(self, request, *args, **kwargs):
        context = {}
        context['token'] = self.kwargs['token']
        return render(request, self.template_name, context)


class ProgramAPI(generics.ListAPIView):
    serializer_class = ProgramSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = ProgramModel.objects.filter(is_active=True).order_by("-id")

class PackageAPI(generics.ListAPIView):
    serializer_class = PackageSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = PackageModel.objects.filter(is_active=True).order_by("-id")

class CalendarAPI(generics.ListAPIView):
    serializer_class = CalendarSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = CalendarModel.objects.filter(created_on__month=timezone.now().month).order_by("-id")

class OrderAPI(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user).order_by("-id")