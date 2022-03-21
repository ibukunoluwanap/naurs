from django.contrib import admin
from .models import ProgramModel, ProgramBenefitModel, ProgramEnquiryModel, ProgramPaymentModel

admin.site.register(ProgramModel)
admin.site.register(ProgramEnquiryModel)
admin.site.register(ProgramBenefitModel)
admin.site.register(ProgramPaymentModel)