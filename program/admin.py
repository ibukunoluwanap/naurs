from django.contrib import admin
from .models import ProgramModel, ProgramBenefitModel, ProgramEnquiryModel

admin.site.register(ProgramModel)
admin.site.register(ProgramBenefitModel)
admin.site.register(ProgramEnquiryModel)