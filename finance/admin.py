from django.contrib import admin
from finance.models import BillingAddressModel, OrderModel, TransactionHistoryModel, WalletModel

admin.site.register(WalletModel)
admin.site.register(BillingAddressModel)
admin.site.register(OrderModel)
admin.site.register(TransactionHistoryModel)
