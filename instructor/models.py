from django.db import models
from program.models import ProgramModel
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model

# setting User model
User = get_user_model()

# instructor modal
class InstructorModel(models.Model):
    user = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE)
    program = models.ManyToManyField(ProgramModel, verbose_name="program")
    role = models.CharField("role", max_length=100, blank=False, null=False)
    about = HTMLField()
    created_on = models.TimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'InstructorModel'
        verbose_name_plural = 'InstructorModels'

    def __str__(self):
        return f"{self.user.email}"