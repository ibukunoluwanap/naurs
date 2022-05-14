from django import forms
from home.models import ListingModel, CalendarModel, StudioUserModel
from instructor.models import InstructorModel
from program.models import ProgramModel

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
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M")

# listing form
class ListingForm(forms.ModelForm):
    class Meta:
        model = ListingModel
        exclude = ['created_on',]

# program calendar form
class CalendarForm(forms.ModelForm):
    start_at = DateTimeLocalField()
    end_at = DateTimeLocalField()

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
