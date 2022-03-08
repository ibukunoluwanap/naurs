from django.contrib import admin
from .models import ProgramModel, ProgramBenefitModel, ProgramEnquiryModel, ProgramPaymentModel

class ProgramBenefitInline(admin.TabularInline):
    model = ProgramBenefitModel

class ProgramEnquiryInline(admin.StackedInline):
    model = ProgramEnquiryModel

class ProgramAdmin(admin.ModelAdmin):
   inlines = [ProgramBenefitInline, ProgramEnquiryInline]

admin.site.register(ProgramModel, ProgramAdmin)
admin.site.register(ProgramPaymentModel)