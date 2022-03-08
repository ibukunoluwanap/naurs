from django import forms
from tinymce.widgets import TinyMCE
from .models import ProgramEnquiryModel, ProgramPaymentModel

# program enquiry form
class ProgramEnquiryForm(forms.ModelForm):
    name = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    phone_number = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput, help_text='Required. Inform a valid email address.')
    enquiry = forms.CharField(max_length=250, required=True, widget=forms.Textarea)

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