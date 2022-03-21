from urllib import request
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# setting User model
User = get_user_model()

# register form
class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput, help_text='Required. Inform a valid email address.')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# login form
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput, help_text='Required. Inform a valid email address.')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

# create user admin
class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# update user admin
class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active', 'admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

# update user form
class UpdateUserForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput)
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput, help_text='Required. Inform a valid email address.')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'last_name', 'email', 'password']

# update admin form
class UpdateAdminForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput)
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput, help_text='Required. Inform a valid email address.')
    admin = forms.BooleanField(initial=True)

    class Meta:
        model = User
        exclude = ['last_login', 'date_joined', 'password']

# update password
class UpdatePasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['password',]