from rest_framework import serializers
from account.serializers import UserSerializer
from instructor.models import InstructorModel

# Instructor Serializer
class InstructorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = InstructorModel
        fields = "__all__"
        depth = 4

