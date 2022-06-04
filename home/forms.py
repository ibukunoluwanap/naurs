from django import forms
from home.models import ListingModel, CalendarModel, NotificationModel, StudioUserModel
from instructor.models import InstructorModel
from program.models import ProgramModel
from tinymce.widgets import TinyMCE
from django.utils import timezone

def validate_date(date):
    if date < timezone.now():
        raise forms.ValidationError("Date cannot be in the past")
        
# custom datetime input
class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"

# custom datetime field
class DateTimeLocalField(forms.DateTimeField):
    input_formats = [
        "%Y-%m-%dT%H:%M:%S", 
        "%Y-%m-%dT%H:%M:%S.%f", 
        "%Y-%m-%dT%H:%M"
    ]
    initial=timezone.now()
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M")

# listing form
class ListingForm(forms.ModelForm):
    class Meta:
        model = ListingModel
        exclude = ['created_on',]

# program calendar form
class CalendarForm(forms.ModelForm):
    start_at = DateTimeLocalField(validators=[validate_date])
    end_at = DateTimeLocalField(validators=[validate_date])

    def __init__(self, *args, **kwargs):
        super(CalendarForm, self).__init__(*args, **kwargs)
        programs = ProgramModel.objects.order_by('-id')
        instructors = InstructorModel.objects.order_by('-id')
        self.fields['program'].choices = [(program.pk, program.title) for program in programs]
        self.fields['instructor'].choices = [(instructor.pk, instructor.user.get_full_name()) for instructor in instructors]

    class Meta:
        model = CalendarModel
        exclude = ['created_on']

# studio user form
class StudioUserForm(forms.ModelForm):
    class Meta:
        model = StudioUserModel
        exclude = ['studio', 'created_on']

#  notification form
class NotificationForm(forms.ModelForm):
    message = forms.CharField(required=True, widget=TinyMCE(attrs={'cols': 10, 'rows': 27}))
    class Meta:
        model = NotificationModel
        exclude = ['student_read', 'created_on']
