from django.db import models
from tinymce.models import HTMLField

# about modal
class AboutModel(models.Model):
    about = HTMLField()
    mission = HTMLField()
    vision = HTMLField()
    value = HTMLField()
    created_on = models.TimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'AboutModel'
        verbose_name_plural = 'AboutModels'

    def __str__(self):
        return "About naurs"