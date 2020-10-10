import datetime

import pytest

from ctrack.register.models import MeetingEvent

pytestmark = pytest.mark.django_db


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
    assert e.created_date.hour == now.hour
    assert e.modified_date.day == now.day
    assert e.modified_date.hour == now.hour
