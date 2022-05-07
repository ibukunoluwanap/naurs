from django.db import models
from django.contrib.auth import get_user_model

# setting User model
User = get_user_model()

# student modal
class StudentModel(models.Model):
    user = models.OneToOneField(User, verbose_name="user", on_delete=models.CASCADE)
    address = models.CharField("address", max_length=250, blank=True, null=True)
    dob = models.DateField("date of birth", max_length=8, blank=True, null=True)
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.user}"