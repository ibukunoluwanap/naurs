from django.db import models
from tinymce.models import HTMLField

# program modal
class ProgramModel(models.Model):
    image = models.FileField("image", upload_to="program/", max_length=100, blank=False, null=False)
    title = models.CharField("title", max_length=100, blank=False, null=False)
    price = models.CharField("price", max_length=100, blank=False, null=False)
    info = HTMLField()
    created_on = models.TimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'ProgramModel'
        verbose_name_plural = 'ProgramModels'

    def __str__(self):
        return f"{self.title} program program"

# program modal
class ProgramBenefitModel(models.Model):
    program = models.ForeignKey(ProgramModel, verbose_name="program", on_delete=models.CASCADE)
    benefit = models.CharField("name", max_length=100, blank=False, null=False)
    created_on = models.TimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'ProgramBenefitModel'
        verbose_name_plural = 'ProgramBenefitModels'

    def __str__(self):
        return f"{self.program} benefit"

# program enquiry modal
class ProgramEnquiryModel(models.Model):
    program = models.ForeignKey(ProgramModel, verbose_name="program", on_delete=models.CASCADE)
    name = models.CharField("name", max_length=100, blank=False, null=False)
    email = models.EmailField("email address", max_length=254, blank=False, null=False)
    phone_number = models.CharField("phone number", max_length=100, blank=False, null=False)
    enquiry = models.TextField("enquiry", max_length=250, blank=False, null=False)
    created_on = models.TimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'ProgramEnquiryModel'
        verbose_name_plural = 'ProgramEnquiryModels'

    def __str__(self):
        return f"{self.program} enquiry from {self.name}"