from django import forms
from tinymce.widgets import TinyMCE

from program.models import ProgramModel
from .models import InstructorModel
from django.forms import inlineformset_factory

# instructor form
class InstructorForm(forms.ModelForm):
    program = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=ProgramModel.objects.all())
    about = forms.CharField(required=True, widget=TinyMCE(attrs={'cols': 10, 'rows': 22}))

    class Meta:
        model = InstructorModel
        exclude = ['user', 'created_on']