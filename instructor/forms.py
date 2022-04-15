from django import forms
from tinymce.widgets import TinyMCE
from .models import InstructorModel
from django.contrib.auth import get_user_model

# setting User model
User = get_user_model()

# instructor form
class InstructorForm(forms.ModelForm):
    about = forms.CharField(required=True, widget=TinyMCE(attrs={'cols': 10, 'rows': 27}))

    class Meta:
        model = InstructorModel
        exclude = ['user', 'created_on']