from django.contrib import admin
from .models import OfferModel, BookOfferModel, FreeTrialOfferModel

class BookOfferInline(admin.TabularInline):
    model = BookOfferModel

class OfferAdmin(admin.ModelAdmin):
   inlines = [BookOfferInline,]

admin.site.register(OfferModel, OfferAdmin)
admin.site.register(FreeTrialOfferModel)