from rest_framework import serializers
from account.serializers import UserSerializer
from finance.models import OrderModel
from program.serializers import PackageSerializer, ProgramSerializer

# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    package = PackageSerializer(many=True)
    program = ProgramSerializer(many=True)
    class Meta:
        model = OrderModel
        fields = "__all__"
        depth = 4
