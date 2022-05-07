from django import forms
from student.models import StudentModel

# student form
class StudentForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    
    class Meta:
        model = StudentModel
        exclude = ['user', 'created_on']