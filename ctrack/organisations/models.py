from django.db import models

# Create your models here.
from django.urls import reverse
from slugify import slugify


class Address(models.Model):
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255)
    line3 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    other_details = models.CharField(max_length=255)


class Organisation(models.Model):
    name = models.CharField(max_length=255, blank=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("organisations:detail", kwargs={"name": self.slugify_name()})

    def slugify_name(self):
        return slugify(self.name)
