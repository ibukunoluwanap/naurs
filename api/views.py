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
from finance.models import BillingAddressModel, OrderModel, TransactionHistoryModel, WalletModel
from finance.serializers import BillingAddressSerializer, OrderSerializer, TransactionHistorySerializer, WalletSerializer
from home.models import CalendarModel, NotificationModel
from home.serializers import CalendarSerializer, NotificationSerializer
from instructor.models import InstructorModel, InstructorNotificationModel
from instructor.serializers import InstructorNotificationSerializer, InstructorSerializer
from naurs.settings import EMAIL_HOST_USER, DOMAIN
import socket
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from rest_framework import status
from django.views.generic import View
from program.models import PackageModel, ProgramModel
from program.serializers import PackageSerializer, ProgramSerializer
from django.utils import timezone
from student.models import StudentModel
from student.serializers import StudentSerializer

User = get_user_model()

# user API
class UserAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(UserAPI, self).get_serializer(*args, **kwargs)

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
class ChangePasswordAPI(generics.UpdateAPIView):
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

class PasswordResetConfirmAPI(View):
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

class WalletUpdateAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WalletSerializer
    permission_classes = (permissions.IsAuthenticated,)
    model = WalletModel

    def get_object(self):
        try:
            return WalletModel.objects.get(user=self.request.user)
        except WalletModel.DoesNotExist:
            return;

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(WalletUpdateAPI, self).get_serializer(*args, **kwargs)

class BillingAddressUpdateAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BillingAddressSerializer
    permission_classes = (permissions.IsAuthenticated,)
    model = BillingAddressModel

    def get_object(self):
        try:
            return BillingAddressModel.objects.get(user=self.request.user)
        except BillingAddressModel.DoesNotExist:
            return;

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(BillingAddressUpdateAPI, self).get_serializer(*args, **kwargs)

class OrderAPI(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user).order_by("-id")

class TransactionHistoryAPI(generics.ListAPIView):
    serializer_class = TransactionHistorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return TransactionHistoryModel.objects.filter(wallet__user=self.request.user).order_by("-id")

class StudentUpdateAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    model = StudentModel

    def get_object(self):
        return StudentModel.objects.get(user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(StudentUpdateAPI, self).get_serializer(*args, **kwargs)

class InstructorAPI(generics.ListAPIView):
    serializer_class = InstructorSerializer
    permission_classes = (permissions.IsAuthenticated,)
    model = InstructorModel

    def get_queryset(self):
        return InstructorModel.objects.order_by("-id")

class InstructorUpdateAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InstructorSerializer
    permission_classes = (permissions.IsAuthenticated,)
    model = InstructorModel

    def get_object(self):
        return InstructorModel.objects.get(user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(InstructorUpdateAPI, self).get_serializer(*args, **kwargs)

class InstructorNotificationCreateAPI(generics.CreateAPIView):
    serializer_class = InstructorNotificationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    model = InstructorNotificationModel

class InstructorNotificationAPI(generics.ListAPIView):
    serializer_class = InstructorNotificationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return InstructorNotificationModel.objects.filter(student__user=self.request.user).order_by("-id")

class NotificationAPI(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return NotificationModel.objects.order_by("-id")

class GetPackageAPI(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        package_type = self.kwargs['package_type']
        package = PackageModel.objects.get(id=self.kwargs['package_id'])
        wallet = WalletModel.objects.get(user=request.user)

        if package_type == "bonus":
            for program in package.program.all():
                pass

            if wallet.balance < package.initial_price:
                response = {
                    'status': 'error',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Insufficient wallet balance! Please "TOP UP" your wallet'
                }
                return Response(response)
            
            # update price
            new_wallet_balance = wallet.balance - package.initial_price
            wallet_balance = new_wallet_balance + package.bonus_price

            # updating wallet
            wallet.balance = wallet_balance
            wallet.save()

            # create order
            if request.user.ordermodel_set.filter(package=package).exists():
                # update price
                new_wallet_balance = wallet.balance + package.initial_price
                wallet_balance = new_wallet_balance - package.bonus_price

                # updating wallet
                wallet.balance = wallet_balance
                wallet.save()

                response = {
                    'status': 'warning',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'This package is currently active on your account'
                }
                return Response(response)

            order = OrderModel.objects.create(
                user = request.user,
                amount = package.initial_price,
                status = True,
                sessions = package.sessions,
            )

            order.package.add(package)
            order.program.add(*package.program.all())

            student = StudentModel.objects.get(user=request.user)
            program.students.add(student)

            program.save()

            response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': f'Successfully purchased {package.name}! Please refresh screen'
                }
            return Response(response)

