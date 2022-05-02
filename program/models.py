from django.db import models
from tinymce.models import HTMLField
from instructor.models import InstructorModel
from student.models import StudentModel

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
    price = models.FloatField(default=0.00)
    total_space = models.PositiveIntegerField()
    students = models.ManyToManyField(StudentModel, verbose_name="students")
    instructors = models.ManyToManyField(InstructorModel, verbose_name="instructors")
    is_active = models.BooleanField(verbose_name="activate", default=True)
    content = HTMLField()
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        return f"{self.title}"

# program benefit modal
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

# package modal
class PackageModel(models.Model):
    image = models.FileField("image", upload_to="package/", max_length=100, blank=False, null=False)
    name = models.CharField("title", max_length=100, blank=False, null=False)
    initial_price = models.FloatField(default=0.00)
    bonus_price = models.FloatField(default=0.00)
    sessions = models.PositiveIntegerField(default=0)
    kids_sessions = models.PositiveIntegerField(default=0)
    senior_citizen_sessions = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(verbose_name="activate", default=True)
    program = models.ManyToManyField(ProgramModel, verbose_name="class")
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        return f"{self.name}"
