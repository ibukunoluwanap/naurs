from django.contrib import admin
from .models import ProgramModel, ProgramBenefitModel

admin.site.register(ProgramModel)
admin.site.register(ProgramBenefitModel)