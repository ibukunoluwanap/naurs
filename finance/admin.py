from django.contrib import admin
from finance.models import BillingAddressModel, WalletModel

admin.site.register(WalletModel)
admin.site.register(BillingAddressModel)
