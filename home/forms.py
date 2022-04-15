from django import forms
from home.models import ListingModel, CalendarModel

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
    class Meta:
        model = CalendarModel
        exclude = ['program', 'created_on']