from rest_framework import serializers
from program.models import PackageModel, ProgramModel

# Program Serializer
class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramModel
        fields = "__all__"

# Package Serializer
class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageModel
        fields = "__all__"
