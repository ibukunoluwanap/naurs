from django import forms
from home.models import ListingModel

# listing form
class ListingForm(forms.ModelForm):
    class Meta:
        model = ListingModel
        exclude = ['created_on',]