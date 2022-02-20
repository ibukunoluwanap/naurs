from django.db import models

# Create your models here.
class FreeTrialOfferModel(models.Model):
    name = models.CharField("name", max_length=100)
    phone_number = models.CharField("phone number", max_length=100)
    email = models.EmailField("email address", max_length=254)
    created_on = models.TimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'OfferModel'
        verbose_name_plural = 'OfferModels'

    def __str__(self):
        return self.name
