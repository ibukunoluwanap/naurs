from django.db import models
from instructor.models import InstructorModel
from program.models import ProgramModel

LISTING_CATEGORY = (
    ("Music", "Music"),
    ("Gymnastic", "Gymnastic"),
    ("Yoga", "Yoga"),
    ("Art", "Art"),
)


# Listing modal
class ListingModel(models.Model):
    category = models.CharField("category", choices=LISTING_CATEGORY, default=LISTING_CATEGORY[0], max_length=100, blank=False, null=False)
    listing = models.CharField("listing", max_length=100, blank=False, null=False)
    coming_soon = models.BooleanField(default=False)
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Listing'
        verbose_name_plural = 'Listings'

    def __str__(self):
        return f"{self.listing}"

# program calendar modal
class CalendarModel(models.Model):
    program = models.ForeignKey(ProgramModel, verbose_name="class", on_delete=models.CASCADE)
    instructor = models.ForeignKey(InstructorModel,  verbose_name="instructor", on_delete=models.CASCADE)
    start_at = models.DateTimeField("start_at")
    end_at = models.DateTimeField("end_at")
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Class Calendar'
        verbose_name_plural = 'Class Calendars'

    def __str__(self):
        return f"{self.program} calendar"

# studio modal
class StudioModel(models.Model):
    name = models.CharField(verbose_name="name", max_length=255)
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Studio'
        verbose_name_plural = 'Studios'

    def __str__(self):
        return f"{self.name}"

# studio user modal
class StudioUserModel(models.Model):
    studio = models.ForeignKey(StudioModel, verbose_name="studio", on_delete=models.CASCADE)
    full_name = models.CharField(verbose_name="Full name", max_length=200)
    email = models.EmailField(verbose_name='email address', max_length=255)
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'Studio User'
        verbose_name_plural = 'Studio Users'

    def __str__(self):
        return f"{self.full_name} at {self.studio}"