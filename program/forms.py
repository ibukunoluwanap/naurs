from django import forms
from tinymce.widgets import TinyMCE
from .models import ProgramBenefitModel, ProgramEnquiryModel, ProgramModel, ProgramPaymentModel
from django.forms import inlineformset_factory

# program form
class ProgramForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput)
    info = forms.CharField(required=True, widget=TinyMCE(attrs={'cols': 10, 'rows': 22}))

    class Meta:
        model = ProgramModel
        exclude = ['created_on']

# program benefit form
class ProgramBenefitForm(forms.ModelForm):
    class Meta:
        model = ProgramBenefitModel
        exclude = ['program', 'created_on']

# program benefit inline formset
ProgramBenefitInlineFormset = inlineformset_factory(
    ProgramModel,
    ProgramBenefitModel,
    form=ProgramBenefitForm,
    extra=6,
    # max_num=5,
    # fk_name=None,
    # fields=None, exclude=None, can_order=False,
    # can_delete=True, max_num=None, formfield_callback=None,
    # widgets=None, validate_max=False, localized_fields=None,
    # labels=None, help_texts=None, error_messages=None,
    # min_num=None, validate_min=False, field_classes=None
)

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