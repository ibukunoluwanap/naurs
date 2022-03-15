from django import forms
from tinymce.widgets import TinyMCE
from .models import BookOfferModel, OfferModel, FreeTrialOfferModel

# offer form
class OfferForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput)
    content = forms.CharField(required=True, widget=TinyMCE(attrs={'cols': 10, 'rows': 20}))
    class Meta:
        model = OfferModel
        exclude = ['created_on',]

# book offer form
class BookOfferForm(forms.ModelForm):
    name = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    phone_number = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput, help_text='Required. Inform a valid email address.')

    class Meta:
        model = BookOfferModel
        exclude = ['offer', 'created_on']

# free trial offer form
class FreeTrialOfferForm(forms.ModelForm):
    name = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    phone_number = forms.CharField(max_length=30, required=True, widget=forms.TextInput)
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput, help_text='Required. Inform a valid email address.')

    class Meta:
        model = FreeTrialOfferModel
        exclude = ['created_on',]