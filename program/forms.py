from django import forms
from tinymce.widgets import TinyMCE
from .models import ProgramEnquiryModel

# program enquiry form
class ProgramEnquiryForm(forms.ModelForm):
    name = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    phone_number = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput, help_text='Required. Inform a valid email address.')
    enquiry = forms.CharField(max_length=250, required=True, widget=forms.Textarea)

    class Meta:
        model = ProgramEnquiryModel
        exclude = ['program', 'created_on']