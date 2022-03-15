from django import forms
from tinymce.widgets import TinyMCE
from .models import AboutModel

# about form
class AboutForm(forms.ModelForm):
    mission = forms.CharField(required=True, widget=TinyMCE(attrs={'cols': 10, 'rows': 20}))
    vision = forms.CharField(required=True, widget=TinyMCE(attrs={'cols': 10, 'rows': 20}))
    value = forms.CharField(required=True, widget=TinyMCE(attrs={'cols': 10, 'rows': 20}))
    
    class Meta:
        model = AboutModel
        exclude = ['created_on',]