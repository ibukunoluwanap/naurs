from django.contrib import admin
from finance.models import BillingAddressModel, OrderModel, WalletModel

admin.site.register(WalletModel)
admin.site.register(BillingAddressModel)
admin.site.register(OrderModel)
