from django.contrib import admin
from instructor.models import ProgramModel, ProgramBenefitModel

admin.site.register(ProgramModel, ProgramBenefitModel)