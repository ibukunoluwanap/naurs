from django.contrib import admin
from .models import PackageModel, ProgramModel, ProgramBenefitModel, ProgramEnquiryModel

admin.site.register(ProgramModel)
admin.site.register(ProgramEnquiryModel)
admin.site.register(ProgramBenefitModel)
admin.site.register(PackageModel)