from django.db import models
from django.contrib.auth import get_user_model

# setting User model
User = get_user_model()

# wallet modal
class WalletModel(models.Model):
    user = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE)
    balance = models.FloatField(default=0.00)
    updated_on = models.DateTimeField("updated on", auto_now=True)

    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallet'

    def __str__(self):
        return f"{self.user}"

# billing address modal
class BillingAddressModel(models.Model):
    user = models.OneToOneField(User, verbose_name="user", on_delete=models.CASCADE)
    street_address = models.CharField("street address", max_length=250, blank=False, null=False)
    city_town = models.CharField("city/town", max_length=100, blank=False, null=False)
    country = models.CharField("country", max_length=250, blank=False, null=False)
    zip_code = models.CharField("zip code", max_length=50, blank=False, null=False)
    updated_on = models.DateTimeField("updated on", auto_now=True)

    class Meta:
        verbose_name = 'BillingAddress'
        verbose_name_plural = 'BillingAddresses'

    def __str__(self):
        return f"{self.user}"

