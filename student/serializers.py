from rest_framework import serializers
from account.serializers import UserSerializer
from student.models import StudentModel

# Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = StudentModel
        fields = "__all__"
        depth = 4

