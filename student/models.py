from django.db import models
from django.contrib.auth import get_user_model

# setting User model
User = get_user_model()

# student modal
class StudentModel(models.Model):
    user = models.OneToOneField(User, verbose_name="user", on_delete=models.CASCADE)
    sessions = models.PositiveIntegerField(default=0)
    kids = models.BooleanField(default=False)
    senior_citizen = models.BooleanField(default=False)
    sessions = models.PositiveIntegerField(default=0)
    kids_sessions = models.PositiveIntegerField(default=0)
    senior_citizen_sessions = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.user}"