from django import forms
from tinymce.widgets import TinyMCE
from .models import OfferModel, FreeTrialOfferModel

# offer form
class OfferForm(forms.ModelForm):
    title = forms.CharField(max_length=250, required=True, widget=forms.TextInput)
    content = forms.CharField(widget=TinyMCE(attrs={'required': True, 'cols': 30, 'rows': 10}))
    class Meta:
        model = OfferModel
        exclude = ['created_on',]

# free trial offer form
class FreeTrialOfferForm(forms.ModelForm):
    name = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    phone_number = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput, help_text='Required. Inform a valid email address.')

    class Meta:
        model = FreeTrialOfferModel
        exclude = ['created_on',]