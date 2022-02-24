from django.contrib import admin
from instructor.models import OfferModel, BookOfferModel

admin.site.register(OfferModel, BookOfferModel)