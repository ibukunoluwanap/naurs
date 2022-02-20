from django import forms
from .models import FreeTrialOfferModel

# free trial offer form
class FreeTrialOfferForm(forms.ModelForm):
    name = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    phone_number = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput, help_text='Required. Inform a valid email address.')

    class Meta:
        model = FreeTrialOfferModel
        exclude = ['created_on',]