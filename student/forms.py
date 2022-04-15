from django import forms
from student.models import StudentModel

# student form
class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentModel
        exclude = ['user', 'created_on']