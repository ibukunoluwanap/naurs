from email.policy import default
from django.db import models
from django.forms import BooleanField
from tinymce.models import HTMLField

# program category
PROGRAM_CATEGORY = (
    ("Music", "Music"),
    ("Dance", "Dance"),
    ("Fine Arts", "Fine Arts"),
    ("Fitness", "Fitness"),
)

# program modal
class ProgramModel(models.Model):
    image = models.FileField("image", upload_to="program/", max_length=100, blank=False, null=False)
    category = models.CharField("category", choices=PROGRAM_CATEGORY, default=PROGRAM_CATEGORY[0], max_length=100, blank=False, null=False)
    title = models.CharField("title", max_length=100, blank=False, null=False)
    price = models.PositiveIntegerField()
    total_space = models.PositiveIntegerField()
    info = HTMLField()
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Program'
        verbose_name_plural = 'Programs'

    def __str__(self):
        return f"{self.title} program program"

# program modal
class ProgramBenefitModel(models.Model):
    program = models.ForeignKey(ProgramModel, verbose_name="program", on_delete=models.CASCADE)
    benefit = models.CharField("name", max_length=100, blank=False, null=False)
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Program Benefit'
        verbose_name_plural = 'Program Benefits'

    def __str__(self):
        return f"{self.program} benefit"

# program enquiry modal
class ProgramEnquiryModel(models.Model):
    program = models.ForeignKey(ProgramModel, verbose_name="program", on_delete=models.CASCADE)
    name = models.CharField("name", max_length=100, blank=False, null=False)
    email = models.EmailField("email address", max_length=254, blank=False, null=False)
    phone_number = models.CharField("phone number", max_length=100, blank=False, null=False)
    enquiry = models.TextField("enquiry", max_length=250, blank=False, null=False)
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Program Enquiry'
        verbose_name_plural = 'Program Enquiries'

    def __str__(self):
        return f"{self.program.title} enquiry from {self.name}"

class ProgramPayment(models.Model):
    program = models.ForeignKey(ProgramModel, verbose_name="program", on_delete=models.CASCADE)
    first_name = models.CharField("first name", max_length=100, blank=False, null=False)
    last_name = models.CharField("last name", max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=255, blank=False, null=False)
    completed = models.BooleanField(default=False)
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'ProgramPayment'
        verbose_name_plural = 'ProgramPayments'

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"Payment by {self.get_full_name()}"