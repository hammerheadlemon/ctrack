from datetime import date as std_date
from typing import Optional, Dict

from django.contrib.auth import get_user_model
from django.db import models

from ctrack.caf.models import CAF
from ctrack.organisations.models import Person

def _style_descriptor(days: int) -> str:
    if days < 1:
        return "red"
    elif 0 < days < 5:
        return "orange"
    else:
        return "black"


def _day_string(days: int) -> str:
    if days < 1 or days > 1:
        return "days"
    else:
        return "day"

class EngagementType(models.Model):
    """
    Examples here are Phone, Email, Letter, Site visit, Meeting, Audit, Inspection, etc.
    Also official instruments such as designation letters, Information Notices, etc.
    """

    descriptor = models.CharField(max_length=50, blank=False)
    enforcement_instrument = models.BooleanField(default=False)
    regulation_reference = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.descriptor


class EngagementEvent(models.Model):
    """
    Involves multiple people, such as a meeting, phone call, etc.
    """

    def get_sentinel_user():
        """
        We need this so that we can ensure models.SET() is applied with a callable
        to handle when Users are deleted from the system, preventing the EngagementEvent
        objects related to them being deleted also.
        """
        return get_user_model().objects.get_or_create(username="DELETED USER")[0]

    type = models.ForeignKey(EngagementType, on_delete=models.CASCADE)
    short_description = models.CharField(
        max_length=50, help_text="Short description of the event"
    )
    participants = models.ManyToManyField(Person)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user))
    date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    document_link = models.URLField(max_length=1000, blank=True, null=True)
    response_date_requested = models.DateField(blank=True, null=True)
    response_received = models.DateField(blank=True, null=True)
    related_caf = models.ForeignKey(
        CAF, blank=True, on_delete=models.CASCADE, null=True
    )
    comments = models.TextField(max_length=1000, blank=True, null=True)

    def days_to_response_due(self) -> Optional[Dict[int, str]]:
        if self.response_date_requested:
            today = std_date.today()
            diff = self.response_date_requested - today
            return dict(days=diff.days, descriptor=_style_descriptor(diff.days), day_str=_day_string(diff.days))
        else:
            return None

    def __str__(self):
        d = self.date.date()
        iso_format_date = d.isoformat()
        return f"{iso_format_date} | {self.type.descriptor} | {self.short_description}"


