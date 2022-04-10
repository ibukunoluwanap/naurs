from django import forms
from instructor.models import InstructorModel
from program.forms import CustomMultipleChoiceField
from program.models import ProgramModel
from student.models import StudentModel

# student form
class StudentForm(forms.ModelForm):
    instructor = CustomMultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple, queryset=InstructorModel.objects.all())
    program = CustomMultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple, queryset=ProgramModel.objects.all())

    class Meta:
        model = StudentModel
        exclude = ['user', 'created_on']