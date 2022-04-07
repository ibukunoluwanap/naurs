from django import forms
from program.forms import CustomMultipleChoiceField
from program.models import ProgramModel
from student.models import StudentModel

# student form
class StudentForm(forms.ModelForm):
    program = CustomMultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple, queryset=ProgramModel.objects.all())

    class Meta:
        model = StudentModel
        exclude = ['created_on']