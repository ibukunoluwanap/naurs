from django import forms
from tinymce.widgets import TinyMCE
from .models import ProgramBenefitModel, ProgramEnquiryModel, ProgramModel, ProgramPaymentModel

# program form
class ProgramForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput)
    content = forms.CharField(required=True, widget=TinyMCE(attrs={'cols': 10, 'rows': 20}))

    class Meta:
        model = ProgramModel
        exclude = ['created_on']

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

# program payment form
class ProgramPaymentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput, help_text='Required. Inform a valid email address.')

    class Meta:
        model = ProgramPaymentModel
        exclude = ['program', 'completed', 'created_on']