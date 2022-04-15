from django import forms
from tinymce.widgets import TinyMCE

from instructor.models import InstructorModel
from .models import PackageModel, ProgramBenefitModel, ProgramEnquiryModel, ProgramModel

# program form
class ProgramForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput)
    content = forms.CharField(required=True, widget=TinyMCE(attrs={'cols': 10, 'rows': 20}))
    class Meta:
        model = ProgramModel
        exclude = ['students', 'instructors', 'created_on',]

# program benefit form
class ProgramBenefitForm(forms.ModelForm):
    class Meta:
        model = ProgramBenefitModel
        exclude = ['program', 'created_on']

# program enquiry form
class ProgramEnquiryForm(forms.ModelForm):
    name = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    phone_number = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput, help_text='Required. Inform a valid email address.')
    enquiry = forms.CharField(max_length=500, required=True, widget=forms.Textarea(attrs={"style":"height:150px;"}))

    class Meta:
        model = ProgramEnquiryModel
        exclude = ['program', 'created_on']

# package form
class PackageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput)
    program = forms.ModelMultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple, queryset=ProgramModel.objects.order_by())

    class Meta:
        model = PackageModel
        exclude = ['created_on',]

# instructor list form
class ProgramInstructorForm(forms.ModelForm):
    instructors = forms.ModelMultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple, queryset=InstructorModel.objects.order_by())

    class Meta:
        model = ProgramModel
        fields = ['instructors',]