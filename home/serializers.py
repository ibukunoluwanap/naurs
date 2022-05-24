from rest_framework import serializers
from home.models import CalendarModel
from instructor.serializers import InstructorSerializer
from program.serializers import ProgramSerializer

# Calendar Serializer
class CalendarSerializer(serializers.ModelSerializer):
    program = ProgramSerializer()
    instructor = InstructorSerializer()
    class Meta:
        model = CalendarModel
        fields = "__all__"
        depth = 4
