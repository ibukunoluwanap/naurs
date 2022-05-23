from rest_framework import serializers
from instructor.serializers import InstructorSerializer
from program.models import PackageModel, ProgramModel
from student.serializers import StudentSerializer

# Program Serializer
class ProgramSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)
    instructors = InstructorSerializer(many=True)
    class Meta:
        model = ProgramModel
        fields = "__all__"
        depth = 4

# Package Serializer
class PackageSerializer(serializers.ModelSerializer):
    program = ProgramSerializer(many=True)
    class Meta:
        model = PackageModel
        fields = "__all__"
        depth = 4

