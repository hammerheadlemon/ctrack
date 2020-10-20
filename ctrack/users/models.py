from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from ctrack.organisations.models import Stakeholder, Submode, Organisation


class User(AbstractUser):
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    stakeholder = models.OneToOneField(
        Stakeholder, on_delete=models.CASCADE, null=True, blank=True
    )

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def is_stakeholder(self):
        if self.stakeholder is not None:
            return True
        else:
            return False

    def get_organisation_name(self):
        if self.is_stakeholder:
            return self.stakeholder.person.organisation.name

    def get_lead_inspector_organisations(self):
        return Organisation.objects.filter(lead_inspector=self)

    def get_deputy_lead_inspector_organisations(self):
        return Organisation.objects.filter(deputy_lead_inspector=self)
