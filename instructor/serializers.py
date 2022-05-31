from rest_framework import serializers
from account.serializers import UserSerializer
from instructor.models import InstructorModel, InstructorNotificationModel
from student.serializers import StudentSerializer

# Instructor Serializer
class InstructorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = InstructorModel
        fields = "__all__"
        depth = 4

# Instructor Notification Serializer
class InstructorNotificationSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer()
    student = StudentSerializer()
    class Meta:
        model = InstructorNotificationModel
        fields = "__all__"
        depth = 4

