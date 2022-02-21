from django.db import models
from tinymce.models import HTMLField

# offer modal
class OfferModel(models.Model):
    image = models.FileField("image", upload_to="offers/", max_length=100, blank=None, null=None)
    title = models.CharField("title", max_length=250, blank=None, null=None)
    content = HTMLField()
    created_on = models.TimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'OfferModel'
        verbose_name_plural = 'OfferModels'

    def __str__(self):
        return f"{self.title} offer"

# free trial modal
class FreeTrialOfferModel(models.Model):
    name = models.CharField("name", max_length=100, blank=None, null=None)
    phone_number = models.CharField("phone number", max_length=100, blank=None, null=None)
    email = models.EmailField("email address", max_length=254, blank=None, null=None)
    created_on = models.TimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'FreeTrialOfferModel'
        verbose_name_plural = 'FreeTrialOfferModels'

    def __str__(self):
        return f"free trial from {self.name}"
