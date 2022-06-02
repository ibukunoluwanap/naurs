from rest_framework import serializers
from home.models import CalendarModel, NotificationModel
from instructor.serializers import InstructorSerializer
from program.serializers import ProgramSerializer
from student.serializers import StudentSerializer

# Calendar Serializer
class CalendarSerializer(serializers.ModelSerializer):
    program = ProgramSerializer()
    instructor = InstructorSerializer()
    class Meta:
        model = CalendarModel
        fields = "__all__"
        depth = 4

# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    class Meta:
        model = NotificationModel
        fields = "__all__"
        depth = 4