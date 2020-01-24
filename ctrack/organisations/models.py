from django.db import models

# Create your models here.
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from slugify import slugify


class AddressType(models.Model):
    descriptor = models.CharField(max_length=50)

    def __str__(self):
        return self.descriptor


class Organisation(models.Model):
    name = models.CharField(max_length=255, blank=False)
    slug = AutoSlugField(populate_from=['name'])

    def get_absolute_url(self):
        return reverse("organisations:detail", kwargs={"slug": self.slug})

    def slugify_name(self):
        return slugify(self.name)

    def __str__(self):
        return self.name


class Address(models.Model):
    organisation = models.ForeignKey(
        Organisation, related_name="addresses", on_delete=models.CASCADE, blank=False
    )
    type = models.ForeignKey(
        AddressType, verbose_name="Address Type", on_delete=models.CASCADE, blank=False
    )
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    line3 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    other_details = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return " ".join([self.organisation.name, self.line1])

    class Meta:
        verbose_name_plural = "Addresses"
