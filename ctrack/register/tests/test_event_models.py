import datetime

import pytest
from django.db import IntegrityError

from ctrack.register.models import (
    EventType,
    SingleDateTimeEvent,
    CAFSingleDateEvent,
    CAFTwinDateEvent,
)

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "allowed_type",
    [
        "CAF_INITIAL_CAF_RECEIVED",
        "CAF_FEEDBACK_EMAILED_OES",
        "CAF_RECEIVED",
        "CAF_EMAILED_ROSA",
        "CAF_VALIDATION_SIGN_OFF",
        "CAF_VALIDATION_RECORD_EMAILED_TO_OES",
    ],
)
def test_caf_single_date_events(allowed_type, user, caf):
    now = datetime.datetime.now()
    e = CAFSingleDateEvent.objects.create(
        type_descriptor=allowed_type,
        related_caf=caf,
        short_description="CAF received for X Company",
        date="2020-10-10",
        comments="Nice comments for this event",
        user=user,
    )
    assert e.created_date.day == now.day
    assert e.type_descriptor == allowed_type


@pytest.mark.parametrize(
    "allowed_type", ["CAF_PEER_REVIEW_PERIOD", "CAF_VALIDATION_PERIOD"]
)
def test_caf_twin_date_events(allowed_type, user, caf):
    now = datetime.datetime.now()
    e = CAFTwinDateEvent.objects.create(
        type_descriptor=allowed_type,
        related_caf=caf,
        short_description="CAF received for X Company",
        start_date="2020-10-10",
        end_date="2020-10-25",
        comments="Nice comments for this event",
        user=user,
    )
    assert e.created_date.day == now.day
    assert e.type_descriptor == allowed_type


@pytest.mark.parametrize(
    "allowed_type", ["CAF_PEER_REVIEW_PERIOD", "CAF_VALIDATION_PERIOD"]
)
def test_caf_twin_date_event_no_end_date(allowed_type, user, caf):
    e = CAFTwinDateEvent.objects.create(
        type_descriptor=allowed_type,
        related_caf=caf,
        short_description="CAF received for X Company",
        start_date="2020-10-10",
        comments="Nice comments for this event",
        user=user,
    )
    assert e.end_date is None


@pytest.mark.parametrize(
    "allowed_type", ["CAF_PEER_REVIEW_PERIOD", "CAF_VALIDATION_PERIOD"]
)
def test_caf_twin_date_event_no_start_date_not_allowed(allowed_type, user, caf):
    with pytest.raises(IntegrityError):
        CAFTwinDateEvent.objects.create(
            type_descriptor=allowed_type,
            related_caf=caf,
            short_description="CAF received for X Company",
            end_date="2020-10-10",
            comments="Nice comments for this event",
            user=user,
        )


def test_cannot_add_two_caf_initial_caf_received_events_on_same_date(user, caf):
    CAFSingleDateEvent.objects.create(
        type_descriptor="CAF_INITIAL_CAF_RECEIVED",
        related_caf=caf,
        short_description="CAF received for X Company",
        date="2020-10-10",
        comments="Nice comments for this event",
        user=user,
    )
    with pytest.raises(IntegrityError):
        CAFSingleDateEvent.objects.create(
            type_descriptor="CAF_INITIAL_CAF_RECEIVED",
            related_caf=caf,
            short_description="CAF received for X Company",
            date="2020-10-10",
            comments="Nice comments for this event",
            user=user,
        )


def test_can_email_two_caf_on_same_date(user, caf):
    CAFSingleDateEvent.objects.create(
        type_descriptor="CAF_EMAILED_ROSA",
        related_caf=caf,
        short_description="CAF sent to Rosa for X Company",
        date="2020-10-10",
        comments="Nice comments for this event",
        user=user,
    )
    CAFSingleDateEvent.objects.create(
        type_descriptor="CAF_EMAILED_ROSA",
        related_caf=caf,
        short_description="CAF sent to Rosa for X Company",
        date="2020-10-10",
        comments="Nice comments for this event",
        user=user,
    )


def test_cannot_receive_the_same_caf_on_the_same_day(user, caf):
    CAFSingleDateEvent.objects.create(
        type_descriptor="CAF_RECEIVED",
        related_caf=caf,
        short_description="CAF received to Rosa for X Company",
        date="2020-10-10",
        comments="Nice comments for this event",
        user=user,
    )
    with pytest.raises(IntegrityError):
        CAFSingleDateEvent.objects.create(
            type_descriptor="CAF_RECEIVED",
            related_caf=caf,
            short_description="CAF received to Rosa for X Company",
            date="2020-10-10",
            comments="Nice comments for this event",
            user=user,
        )


def test_event_type_enum():
    assert EventType.MEETING.name == "MEETING"
    assert EventType.PHONE_CALL.name == "PHONE_CALL"
    assert EventType.VIDEO_CALL.name == "VIDEO_CALL"
    assert EventType.CAF_INITIAL_CAF_RECEIVED.name == "CAF_INITIAL_CAF_RECEIVED"
    assert EventType.CAF_FEEDBACK_EMAILED_OES.name == "CAF_FEEDBACK_EMAILED_OES"
    assert EventType.CAF_RECEIVED.name == "CAF_RECEIVED"
    assert EventType.CAF_EMAILED_ROSA.name == "CAF_EMAILED_ROSA"
    assert EventType.CAF_PEER_REVIEW_PERIOD.name == "CAF_PEER_REVIEW_PERIOD"
    assert EventType.CAF_VALIDATION_PERIOD.name == "CAF_VALIDATION_PERIOD"
    assert EventType.CAF_VALIDATION_SIGN_OFF.name == "CAF_VALIDATION_SIGN_OFF"
    assert (
        EventType.CAF_VALIDATION_RECORD_EMAILED_TO_OES.name
        == "CAF_VALIDATION_RECORD_EMAILED_TO_OES"
    )


@pytest.mark.parametrize("allowed_type", [("PHONE_CALL"), ("MEETING"), ("VIDEO_CALL")])
def test_single_datetime_event(person, user, allowed_type):
    """This tests for phone call, video call and email events"""
    now = datetime.datetime.now()
    event = SingleDateTimeEvent.objects.create(
        type_descriptor=allowed_type,
        short_description="Important event",
        datetime="2020-10-10T15:00",
        comments="Comments on important event",
        # location is optional
        user=user,
    )
    event.participants.add(person)
    assert event.type_descriptor == allowed_type
    assert person in event.participants.all()
    assert event.created_date.day == now.day


def test_meeting_event(user, person):
    uname = user.name
    now = datetime.datetime.now()
    e = SingleDateTimeEvent.objects.create(
        type_descriptor="Meeting",
        short_description="Big Important Meeting",
        datetime="2020-10-10T15:00",
        comments="Nice comments",
        location="Harvey's House",
        user=user,
    )
    e.participants.add(person)
    assert len(e.participants.all()) == 1
    assert e.type_descriptor == "Meeting"
    assert person in e.participants.all()
    assert e.user.name == uname
    assert e.created_date.day == now.day
    assert e.modified_date.day == now.day
