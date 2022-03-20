from django import forms
from tinymce.widgets import TinyMCE

from program.models import ProgramModel
from .models import InstructorModel
from django.contrib.auth import get_user_model

# setting User model
User = get_user_model()

# instructor form
class InstructorForm(forms.ModelForm):
    program = forms.ModelMultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple, queryset=ProgramModel.objects.all())
    about = forms.CharField(required=True, widget=TinyMCE(attrs={'cols': 10, 'rows': 27}))

    class Meta:
        model = InstructorModel
        exclude = ['created_on']