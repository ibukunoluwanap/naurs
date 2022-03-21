from django.db import models
from instructor.models import InstructorModel
from program.models import ProgramModel
from django.contrib.auth import get_user_model

# setting User model
User = get_user_model()

# student modal
class StudentModel(models.Model):
    user = models.OneToOneField(User, verbose_name="user", null=True, on_delete=models.SET_NULL)
    instructor = models.ForeignKey(InstructorModel, verbose_name="instructor", null=True, on_delete=models.SET_NULL)
    program = models.ManyToManyField(ProgramModel, verbose_name="program")
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.user}"