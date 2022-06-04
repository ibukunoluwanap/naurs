from django.contrib import admin
from finance.models import BillingAddressModel, OrderModel, TicketModel, TransactionHistoryModel, WalletModel

admin.site.register(WalletModel)
admin.site.register(BillingAddressModel)
admin.site.register(OrderModel)
admin.site.register(TransactionHistoryModel)
admin.site.register(TicketModel)
