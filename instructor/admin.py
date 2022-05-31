from django.contrib import admin
from .models import InstructorModel, InstructorNotificationModel

admin.site.register(InstructorModel)
admin.site.register(InstructorNotificationModel)