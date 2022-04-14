from django.db import models
from django.contrib.auth import get_user_model

# setting User model
User = get_user_model()

# wallet modal
class WalletModel(models.Model):
    user = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE)
    balance = models.FloatField()
    updated_on = models.DateTimeField("updated on", auto_now=True)

    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallet'

    def __str__(self):
        return f"{self.title}"
