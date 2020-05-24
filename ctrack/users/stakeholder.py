from django.db import models

from ctrack.organisations.models import Person


class Stakeholder(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
