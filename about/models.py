from django.db import models
from tinymce.models import HTMLField

# about modal
class AboutModel(models.Model):
    about = HTMLField()
    mission = HTMLField()
    vision = HTMLField()
    value = HTMLField()
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'About'
        verbose_name_plural = 'About'

    def __str__(self):
        return "About naurs"