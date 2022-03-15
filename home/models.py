from django.db import models
from program.models import PROGRAM_CATEGORY

# Listing modal
class ListingModel(models.Model):
    category = models.CharField("category", choices=PROGRAM_CATEGORY, default=PROGRAM_CATEGORY[0], max_length=100, blank=False, null=False)
    listing = models.CharField("listing", max_length=100, blank=False, null=False)
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Listing'
        verbose_name_plural = 'Listings'

    def __str__(self):
        return "Naurs listing"