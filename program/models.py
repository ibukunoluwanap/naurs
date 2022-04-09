from django.db import models
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
    is_active = models.BooleanField(verbose_name="activate", default=True)
    start_time = models.DateTimeField("start time")
    content = HTMLField()
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        return f"{self.title}"

# program modal
class ProgramBenefitModel(models.Model):
    program = models.ForeignKey(ProgramModel, verbose_name="class", on_delete=models.CASCADE)
    benefit = models.CharField("benefit", max_length=100, blank=False, null=False)
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Class Benefit'
        verbose_name_plural = 'Class Benefits'

    def __str__(self):
        return f"{self.program} benefit"

# program enquiry modal
class ProgramEnquiryModel(models.Model):
    program = models.ForeignKey(ProgramModel, verbose_name="class", on_delete=models.CASCADE)
    name = models.CharField("name", max_length=100, blank=False, null=False)
    email = models.EmailField("email address", max_length=254, blank=False, null=False)
    phone_number = models.CharField("phone number", max_length=100, blank=False, null=False)
    enquiry = models.TextField("enquiry", max_length=500, blank=False, null=False)
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Class Enquiry'
        verbose_name_plural = 'Class Enquiries'

    def __str__(self):
        return f"{self.program.title} enquiry from {self.name}"

# program payment modal
class ProgramPaymentModel(models.Model):
    program = models.ForeignKey(ProgramModel, verbose_name="class", on_delete=models.CASCADE)
    first_name = models.CharField("first name", max_length=100, blank=False, null=False)
    last_name = models.CharField("last name", max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=255, blank=False, null=False)
    completed = models.BooleanField(default=False)
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Class Payment'
        verbose_name_plural = 'Class Payments'

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"Payment by {self.get_full_name()}"

# package modal
class PackageModel(models.Model):
    image = models.FileField("image", upload_to="package/", max_length=100, blank=False, null=False)
    name = models.CharField("title", max_length=100, blank=False, null=False)
    initial_price = models.PositiveIntegerField()
    bonus_price = models.PositiveIntegerField()
    is_active = models.BooleanField(verbose_name="activate", default=True)
    program = models.ManyToManyField(ProgramModel, verbose_name="class")
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        return f"{self.title}"
