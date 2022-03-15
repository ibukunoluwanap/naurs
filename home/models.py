from email.policy import default
from django.db import models
from django.forms import BooleanField

LISTING_CATEGORY = (
    ("Music", "Music"),
    ("Gymnastic", "Gymnastic"),
    ("Yoga", "Yoga"),
    ("Art", "Art"),
)


# Listing modal
class ListingModel(models.Model):
    category = models.CharField("category", choices=LISTING_CATEGORY, default=LISTING_CATEGORY[0], max_length=100, blank=False, null=False)
    listing = models.CharField("listing", max_length=100, blank=False, null=False)
    coming_soon = models.BooleanField(default=False)
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Listing'
        verbose_name_plural = 'Listings'

    def __str__(self):
        return f"{self.listing}"