from django.contrib import messages
from django.views.generic import View
from account.forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

# register view
class Register(View):
    template_name = "account/register.html"
    form = RegisterForm()

    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            messages.info(request, 'You are logged in already!')
            return redirect('register_page')
        else:
            context["form"] = self.form
            return render(request, self.template_name, context)

    def post(self,request):
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            print(password, email)
            # user = authenticate(email=email, password=password)
            # login(request, user)
            messages.success(request, "Successfully registered")
            return redirect('home_page')
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
