from django.db import models
from django.contrib.auth import get_user_model

from program.models import PackageModel, ProgramModel

# setting User model
User = get_user_model()

# wallet model
class WalletModel(models.Model):
    user = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE)
    balance = models.FloatField(default=0.00)
    updated_on = models.DateTimeField("updated on", auto_now=True)

    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallet'

    def __str__(self):
        return f"{self.user}"

# billing address model
class BillingAddressModel(models.Model):
    user = models.OneToOneField(User, verbose_name="user", on_delete=models.CASCADE)
    street_address = models.CharField("street address", max_length=250, blank=False, null=False)
    city_town = models.CharField("city/town", max_length=100, blank=False, null=False)
    country = models.CharField("country", max_length=250, blank=False, null=False)
    zip_code = models.CharField("zip code", max_length=50, blank=False, null=False)
    updated_on = models.DateTimeField("updated on", auto_now=True)

    class Meta:
        verbose_name = 'Billing Address'
        verbose_name_plural = 'Billing Addresses'

    def __str__(self):
        return f"{self.user}"

# order model
class OrderModel(models.Model):
    user = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE)
    package = models.ManyToManyField(PackageModel, verbose_name="package")
    program = models.ManyToManyField(ProgramModel, verbose_name="class")
    amount = models.FloatField(verbose_name='Amount')
    status = models.BooleanField(default=False, verbose_name='Payment Status')
    sessions = models.PositiveIntegerField(default=0)
    kids_sessions = models.PositiveIntegerField(default=0)
    senior_citizen_sessions = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order by {self.user}"

# Ticket model
class TicketModel(models.Model):
    order = models.ForeignKey(OrderModel, verbose_name="order", on_delete=models.CASCADE)
    ticket_id = models.CharField(verbose_name="ticket id", max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __str__(self):
        return f"Ticket for {self.order.user.get_full_name}"

# Transaction History model
class TransactionHistoryModel(models.Model):
    wallet = models.ForeignKey(WalletModel, verbose_name="user", on_delete=models.CASCADE)
    amount = models.FloatField(verbose_name='Amount')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Transaction History'
        verbose_name_plural = 'Transaction Histories'

    def __str__(self):
        return f"Transaction history for {self.wallet.user}"