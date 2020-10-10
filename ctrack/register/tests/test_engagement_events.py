import pytest
from django.db import models

from ctrack.organisations.models import Person
from ctrack.register.models import EngagementType
from ctrack.register.tests.factories import EngagementTypeFactory

pytestmark = pytest.mark.django_db


def event_type():
    return EngagementTypeFactory.create(descriptor="CAF type")


type = models.ForeignKey(EngagementType, on_delete=models.CASCADE)


class EngagementEventBase(models.Model):
    type_descriptor = "Base Type"
    short_description = models.CharField(
        max_length=50,
        help_text="Short description of the event. Use Comments field for full detail.",
    )
    participants = models.ManyToManyField(Person, null=True, blank=True)
    document_link = models.URLField(
        max_length=1000,
        blank=True,
        null=True,
        help_text="URL only - do not try to drag a file here.",
    )
    response_date_requested = models.DateField(blank=True, null=True)
    comments = models.TextField(max_length=1000, blank=True, null=True,
                                help_text="Use this to provide further detail about the event.")

    class Meta:
        abstract = True


class SingleDateCAFEvent(EngagementEventBase):
    type = models.ForeignKey(
        EngagementType, default=event_type, on_delete=models.CASCADE
    )
    caf_related = models.BooleanField(default=True)
    date = models.DateField(blank=False, null=False)


def test_event_inheritance():
    caf_single_date_event = SingleDateCAFEvent.objects.create(
        short_description="Test Short Description", date="2010-10-10"
    )
    assert isinstance(caf_single_date_event.type, EngagementType)
    assert caf_single_date_event.short_description == "Test Short Description"
    assert caf_single_date_event.caf_related is True
    assert len(caf_single_date_event.participants.all()) == 0
    assert caf_single_date_event.date == "2010-10-10"
    assert caf_single_date_event.document_link is None
    assert caf_single_date_event.response_date_requested is None


class MeetingEventMixin(models.Model):
    participants = models.ManyToManyField(Person, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        abstract = True


class SingleDateTimeEventMixin(models.Model):
    datetime = models.DateTimeField()

    class Meta:
        abstract = True


class MeetingEvent(EngagementEventBase, MeetingEventMixin, SingleDateTimeEventMixin):
    MEETING_CHOICES = [
        ("Meeting", "Meeting")
    ]
    type_descriptor = models.CharField(max_length=50, choices=MEETING_CHOICES)


def test_meeting_event(org_with_people, person):
    e = MeetingEvent.objects.create(
        type_descriptor="Meeting",
        short_description="Big Important Meeting",
        datetime="2020-10-10T15:00",
        comments="Nice comments",
        location="Harvey's House"
    )
    assert len(e.participants.all()) == 0
    assert e.type_descriptor == "Meeting"
