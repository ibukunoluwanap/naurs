from django import forms

from finance.models import BillingAddressModel

# billing address form
class BillingAddressForm(forms.ModelForm):
    zip_code = forms.CharField( widget=forms.TextInput(attrs={'type':'number'}))
    class Meta:
        model = BillingAddressModel
        exclude = ['user', 'updated_on',]