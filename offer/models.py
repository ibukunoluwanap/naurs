from django.db import models
from tinymce.models import HTMLField

# offer modal
class OfferModel(models.Model):
    image = models.FileField("image", upload_to="offers/", max_length=100, blank=False, null=False)
    title = models.CharField("title", max_length=100, blank=False, null=False)
    content = HTMLField()
    created_on = models.TimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'

    def __str__(self):
        return f"{self.title} offer"

# book offer modal
class BookOfferModel(models.Model):
    offer = models.ForeignKey(OfferModel, verbose_name="offer", on_delete=models.CASCADE)
    name = models.CharField("name", max_length=100, blank=False, null=False)
    email = models.EmailField("email address", max_length=254, blank=False, null=False)
    phone_number = models.CharField("phone number", max_length=100, blank=False, null=False)
    created_on = models.TimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Booked Offer'
        verbose_name_plural = 'Booked Offers'

    def __str__(self):
        return f"{self.name} booked {self.offer.title} offer"
        
# free trial modal
class FreeTrialOfferModel(models.Model):
    name = models.CharField("name", max_length=100, blank=False, null=False)
    email = models.EmailField("email address", max_length=254, blank=False, null=False)
    phone_number = models.CharField("phone number", max_length=100, blank=False, null=False)
    created_on = models.TimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Free Trial Offer'
        verbose_name_plural = 'Free Trial Offers'

    def __str__(self):
        return f"free trial from {self.name}"