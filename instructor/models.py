from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
from student.models import StudentModel

# setting User model
User = get_user_model()

# instructor modal
class InstructorModel(models.Model):
    user = models.OneToOneField(User, verbose_name="user", on_delete=models.CASCADE)
    role = models.CharField("role", max_length=100, blank=False, null=False)
    about = HTMLField()
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Instructor'
        verbose_name_plural = 'Instructors'

    def __str__(self):
        return f"{self.user}"

# instructor notification modal
class InstructorNotificationModel(models.Model):
    instructor = models.ForeignKey(InstructorModel, verbose_name="instructor", on_delete=models.CASCADE)
    student = models.ForeignKey(StudentModel, verbose_name="student", on_delete=models.CASCADE)
    instructor_read = models.BooleanField(default=False)
    student_read = models.BooleanField(default=False)
    instructor_msg = HTMLField("message", blank=True, null=True)
    schedule_on = models.DateTimeField("schedule on", blank=True, null=True)
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Instructor Notification'
        verbose_name_plural = 'Instructor Notifications'

    def __str__(self):
        return f"{self.instructor} and {self.student} conversation"