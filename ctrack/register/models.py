import datetime
from datetime import date as std_date
from enum import Enum, auto
from typing import Optional, Dict

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F

from ctrack.caf.models import CAF
from ctrack.organisations.models import Person
from ctrack.users.models import User


class EventType(Enum):
    MEETING = auto()
    PHONE_CALL = auto()
    VIDEO_CALL = auto()
    EMAIL = auto()
    # single date caf events
    CAF_INITIAL_CAF_RECEIVED = auto()
    CAF_FEEDBACK_EMAILED_OES = auto()
    CAF_RECEIVED = auto()
    CAF_EMAILED_ROSA = auto()
    CAF_VALIDATION_SIGN_OFF = auto()
    CAF_VALIDATION_RECORD_EMAILED_TO_OES = auto()
    # twin date caf events
    CAF_PEER_REVIEW_PERIOD = auto()
    CAF_VALIDATION_PERIOD = auto()


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


class AuditableEventBase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # TODO this also needs to include created_by and updated_by attributes
        """Overriding so we can save the dates in here."""
        if not self.pk:
            self.created_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()

        return super().save(*args, **kwargs)


class EventBase(AuditableEventBase):
    short_description = models.CharField(
        max_length=50,
        help_text="Short description of the event. Use Comments field for full detail.",
        blank=False,
    )
    document_link = models.URLField(
        max_length=1000,
        blank=True,
        null=True,
        help_text="URL only - do not try to drag a file here.",
    )
    comments = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        help_text="Use this to provide further detail about the event.",
    )

    class Meta:
        abstract = True


class ThirdPartyEventMixin(models.Model):
    participants = models.ManyToManyField(Person, blank=True)
    location = models.CharField(max_length=100, blank=True)

    class Meta:
        abstract = True


class SingleDateTimeEventMixin(models.Model):
    datetime = models.DateTimeField(blank=False, verbose_name="Date/Time", help_text="DD/MM/YY HH:MM format please!")

    class Meta:
        abstract = True


class SingleDateMixin(models.Model):
    date = models.DateField(blank=False)

    class Meta:
        abstract = True


class TwinDateMixin(models.Model):
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True


class CAFMixin(models.Model):
    related_caf = models.ForeignKey(CAF, on_delete=models.CASCADE, blank=False)

    class Meta:
        abstract = True


class ResponseRequiredMixin(models.Model):
    requested_response_date = models.DateField(blank=True, null=True, help_text="DD/MM/YY format")
    response_received_date = models.DateField(blank=True, null=True, help_text="DD/MM/YY format")

    class Meta:
        abstract = True


class SingleDateTimeEvent(EventBase, ResponseRequiredMixin, ThirdPartyEventMixin, SingleDateTimeEventMixin):
    AVAILABLE_TYPES = [
        (EventType.MEETING.name, "Meeting"),
        (EventType.PHONE_CALL.name, "Phone Call"),
        (EventType.VIDEO_CALL.name, "Video Call"),
        (EventType.EMAIL.name, "Email")
    ]
    type_descriptor = models.CharField(
        blank=False, max_length=50, choices=AVAILABLE_TYPES
    )

    def __str__(self):
        return self.type_descriptor


class CAFSingleDateEvent(EventBase, CAFMixin, SingleDateMixin):
    AVAILABLE_TYPES = [
        (EventType.CAF_INITIAL_CAF_RECEIVED.name, "CAF - Initial CAF Received"),
        (EventType.CAF_FEEDBACK_EMAILED_OES.name, "CAF - Emailed to OES"),
        (EventType.CAF_RECEIVED.name, "CAF - Received"),
        (EventType.CAF_EMAILED_ROSA.name, "CAF - Emailed to Rosa"),
        (EventType.CAF_VALIDATION_SIGN_OFF.name, "CAF - Validation Sign Off"),
        (
            EventType.CAF_VALIDATION_RECORD_EMAILED_TO_OES.name,
            "CAF - Validation Record Sent to OES",
        ),
    ]
    type_descriptor = models.CharField(
        blank=False, max_length=50, choices=AVAILABLE_TYPES
    )

    class Meta:
        constraints = [
            # We can't do multiple CAFSingleDateEvents in a single day unless
            # the type is declared with the Q expression.
            models.UniqueConstraint(
                fields=["date", "type_descriptor"],
                condition=~models.Q(type_descriptor="CAF_EMAILED_ROSA"),
                name="unique_caf_for_date",
            ),
        ]


class CAFTwinDateEvent(EventBase, CAFMixin, TwinDateMixin):
    AVAILABLE_TYPES = [
        (EventType.CAF_PEER_REVIEW_PERIOD.name, "CAF - Peer Review Period"),
        (EventType.CAF_VALIDATION_PERIOD.name, "CAF - Validation Period"),
    ]
    type_descriptor = models.CharField(
        blank=False, max_length=50, choices=AVAILABLE_TYPES
    )

    def __repr__(self):
        return "".join(["CAFTwinDateEvent(", self.type_descriptor, ")"])

    def __str__(self):
        return f"CAFTwinDateEvent({self.type_descriptor}) starting {self.start_date}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_cannot_precede_start_date",
                check=~models.Q(end_date__lt=F("start_date")),
            )
        ]


# OLD CODE BELOW
class EngagementType(models.Model):
    """
    Examples here are Phone, Email, Letter, Site visit, Meeting, Audit, Inspection, etc.
    Also official instruments such as designation letters, Information Notices, etc.
    """

    descriptor = models.CharField(max_length=100, blank=False)
    enforcement_instrument = models.BooleanField(default=False)
    regulation_reference = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(max_length=1000, blank=True, null=True)
    single_date_type = models.BooleanField(default=False, blank=False)

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
        max_length=50,
        help_text="Short description of the event. Use Comments field for full detail.",
    )
    participants = models.ManyToManyField(Person, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user))
    date = models.DateTimeField()
    end_date = models.DateTimeField(
        blank=True, null=True, help_text="Should be used for periodic events."
    )
    document_link = models.URLField(
        max_length=1000,
        blank=True,
        null=True,
        help_text="URL only - do not try to drag a file here.",
    )
    response_date_requested = models.DateField(blank=True, null=True)
    response_received = models.DateField(blank=True, null=True)
    related_caf = models.ForeignKey(
        "caf.CAF",
        blank=True,
        on_delete=models.CASCADE,
        null=True,
        help_text="If the event relates to a CAF, refer to it here.",
    )
    comments = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        help_text="Use this to provide further detail about the event.",
    )

    def days_to_response_due(self) -> Optional[Dict[int, str]]:
        if self.response_date_requested:
            today = std_date.today()
            diff = self.response_date_requested - today
            return dict(
                days=diff.days,
                descriptor=_style_descriptor(diff.days),
                day_str=_day_string(diff.days),
            )
        else:
            return None

    def __str__(self):
        d = self.date.date()
        iso_format_date = d.isoformat()
        return f"{iso_format_date} | {self.type.descriptor} | {self.short_description}"
