from django import forms
from tinymce.widgets import TinyMCE
from .models import InstructorModel, InstructorNotificationModel
from django.contrib.auth import get_user_model

# setting User model
User = get_user_model()

# instructor form
class InstructorForm(forms.ModelForm):
    about = forms.CharField(required=True, widget=TinyMCE(attrs={'cols': 10, 'rows': 27}))

    class Meta:
        model = InstructorModel
        exclude = ['user', 'created_on']

# instructor notification form
class InstructorNotificationForm(forms.ModelForm):
    instructor_msg = forms.CharField(label="Message", required=True, widget=TinyMCE(attrs={'cols': 10, 'rows': 27}))

    class Meta:
        model = InstructorNotificationModel
        exclude = ['instructor', 'instructor_read', 'student_read', 'schedule_on', 'created_on']
