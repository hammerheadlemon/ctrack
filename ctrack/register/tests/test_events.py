import datetime

import pytest

from ctrack.register.models import MeetingEvent, EventType, SingleDateTimeEvent

pytestmark = pytest.mark.django_db


def test_event_type_enum():
    assert EventType.MEETING.name == "MEETING"
    assert EventType.PHONE_CALL.name == "PHONE_CALL"
    assert EventType.VIDEO_CALL.name == "VIDEO_CALL"
    assert EventType.CAF_INITIAL_CAF_RECEIVED.name == "CAF_INITIAL_CAF_RECEIVED"
    assert EventType.CAF_INITIAL_CAF_EMAILED_ROSA.name == "CAF_INITIAL_CAF_EMAILED_ROSA"
    assert EventType.CAF_FEEDBACK_EMAILED_OES.name == "CAF_FEEDBACK_EMAILED_OES"
    assert EventType.CAF_RECEIVED.name == "CAF_RECEIVED"
    assert EventType.CAF_EMAILED_ROSA.name == "CAF_EMAILED_ROSA"
    assert EventType.CAF_PEER_REVIEW_PERIOD.name == "CAF_PEER_REVIEW_PERIOD"
    assert EventType.CAF_VALIDATION_PERIOD.name == "CAF_VALIDATION_PERIOD"
    assert EventType.CAF_VALIDATION_SIGN_OFF.name == "CAF_VALIDATION_SIGN_OFF"
    assert EventType.CAF_VALIDATION_RECORD_EMAILED_TO_OES.name == "CAF_VALIDATION_RECORD_EMAILED_TO_OES"


def test_meeting_event(person, user):
    uname = user.name
    now = datetime.datetime.now()
    e = MeetingEvent.objects.create(
        type_descriptor="Meeting",
        short_description="Big Important Meeting",
        datetime="2020-10-10T15:00",
        comments="Nice comments",
        location="Harvey's House",
        user=user
    )
    e.participants.add(person)
    assert len(e.participants.all()) == 1
    assert e.type_descriptor == "Meeting"
    assert person in e.participants.all()
    assert e.user.name == uname
    assert e.created_date.day == now.day
    assert e.modified_date.day == now.day


def test_single_date_event(person, user):
    """This tests for phone call, video call and email events"""
    now = datetime.datetime.now()
    phone_event = SingleDateTimeEvent.objects.create(
        type_descriptor="Phone Call",
        short_description="Important Phone Call",
        datetime="2020-10-10T15:00",
        comments="Comments on phone call",
        # location is optional
        user=user
    )
    phone_event.participants.add(person)
    assert phone_event.type_descriptor == "Phone Call"
    assert person in phone_event.participants.all()
    assert phone_event.created_date.day == now.day

    video_event = SingleDateTimeEvent.objects.create(
        type_descriptor="Video Call",
        short_description="Important Video Call",
        datetime="2020-10-10T15:00",
        comments="Comments on phone call",
        # location is optional
        user=user
    )
    video_event.participants.add(person)
    assert video_event.type_descriptor == "Video Call"
    assert person in video_event.participants.all()
    assert video_event.created_date.day == now.day
