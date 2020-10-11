import pytest
from django.db import IntegrityError

from ..forms import AddMeetingForm, CAFSingleDateEventForm

pytestmark = pytest.mark.django_db


# TODO this test and the form code needs to be amended to save created_by and update_by
#   on the model


def test_init(user):
    """Here we test that we can pass in the user value from the view.
    We don't want that to be field in the form.
    """
    form = AddMeetingForm(
        {
            "type_descriptor": "MEETING",  # Must be Meeting as that is in the choices param
            "short_description": "Test short description",
            "datetime": "2010-10-10T13:00",
            "comments": "Test Comments",
            "location": "Transient Moabs",
        },
        user=user,
    )
    assert form.is_valid()


def test_meeting_blank_data(user):
    """Missing datetime fields is required. Location is optional"""
    form = AddMeetingForm(
        {
            "type_descriptor": "MEETING",
            "short_description": "Test short description",
            "comments": "Test Comments",
        },
        user=user,
    )
    assert form.is_valid() is False
    assert form.errors == {"datetime": ["This field is required."]}


@pytest.mark.parametrize(
    "allowed_type",
    [
        ("CAF_INITIAL_CAF_RECEIVED"),
        ("CAF_RECEIVED"),
        ("CAF_EMAILED_ROSA"),
    ],
)
def test_caf_initial_received_form(allowed_type, user, caf):
    form = CAFSingleDateEventForm(
        {
            "type_descriptor": allowed_type,
            "related_caf": caf,
            "short_description": "Test Short Description",
            "date": "2010-07-01",
            "comments": "Meaningless comments",
        },
        user=user,
    )
    assert form.is_valid()


def test_cannot_create_two_caf_initial_receipt_events_on_same_day(user, caf):
    form1 = CAFSingleDateEventForm(
        {
            "type_descriptor": "CAF_INITIAL_CAF_RECEIVED",
            "related_caf": caf,
            "short_description": "Test Short Description",
            "date": "2010-07-01",
            "comments": "Meaningless comments",
        },
        user=user,
    )
    form2 = CAFSingleDateEventForm(
        {
            "type_descriptor": "CAF_INITIAL_CAF_RECEIVED",
            "related_caf": caf,
            "short_description": "Test Short Description",
            "date": "2010-07-01",
            "comments": "Meaningless comments",
        },
        user=user,
    )
    assert form1.is_valid()
    form1.save()
    assert form2.is_valid()
    with pytest.raises(IntegrityError):
        form2.save()


def test_can_register_two_send_to_rosa_events_on_same_day(user, caf):
    form1 = CAFSingleDateEventForm(
        {
            "type_descriptor": "CAF_EMAILED_ROSA",
            "related_caf": caf,
            "short_description": "Test Short Description",
            "date": "2010-07-01",
            "comments": "Meaningless comments",
        },
        user=user,
    )
    form2 = CAFSingleDateEventForm(
        {
            "type_descriptor": "CAF_EMAILED_ROSA",
            "related_caf": caf,
            "short_description": "Test Short Description 2",
            "date": "2010-07-01",
            "comments": "Meaningless comments 2",
        },
        user=user,
    )
    assert form1.is_valid()
    assert form2.is_valid()
