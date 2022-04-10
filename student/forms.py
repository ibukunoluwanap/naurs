from django import forms
from instructor.models import InstructorModel
from program.models import ProgramModel
from student.models import StudentModel

# student form
class StudentForm(forms.ModelForm):
    instructor = forms.ModelMultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple, queryset=InstructorModel.objects.all())
    program = forms.ModelMultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple, queryset=ProgramModel.objects.all())

    class Meta:
        model = StudentModel
        exclude = ['user', 'created_on']