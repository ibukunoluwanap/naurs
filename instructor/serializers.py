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
    class Meta:
        model = InstructorNotificationModel
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['instructor'] = InstructorSerializer(instance.instructor).data
        response['student'] = StudentSerializer(instance.student).data
        return response
