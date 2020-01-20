from django.db import models

# Create your models here.
from django.urls import reverse
from slugify import slugify


class Organisation(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def get_absolute_url(self):
        return reverse("organisations:detail", kwargs={"name": self.slugify_name()})

    def slugify_name(self):
        return slugify(self.name)
