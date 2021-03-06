from rest_framework import serializers
from account.serializers import UserSerializer
from finance.models import BillingAddressModel, OrderModel, TicketModel, TransactionHistoryModel, WalletModel
from program.serializers import PackageSerializer, ProgramSerializer

# Wallet Serializer
class WalletSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = WalletModel
        fields = "__all__"
        depth = 4

# BillingAddress Serializer
class BillingAddressSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = BillingAddressModel
        fields = "__all__"
        depth = 4

# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    package = PackageSerializer(many=True)
    program = ProgramSerializer(many=True)
    class Meta:
        model = OrderModel
        fields = "__all__"
        depth = 4

# Transaction History Serializer
class TransactionHistorySerializer(serializers.ModelSerializer):
    wallet = WalletSerializer()
    class Meta:
        model = TransactionHistoryModel
        fields = "__all__"
        depth = 4

# Ticket Serializer Serializer
class TicketSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    class Meta:
        model = TicketModel
        fields = "__all__"
        depth = 4
