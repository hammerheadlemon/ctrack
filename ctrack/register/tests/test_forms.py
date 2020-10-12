import pytest
from django.db import IntegrityError

from ..forms import AddMeetingForm, CAFSingleDateEventForm, CAFTwinDateEventForm

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


def test_cannot_create_disallowed_single_date_event_type_with_form(user):
    form = AddMeetingForm(
        {
            "type_descriptor": "NOT ALLOWED EVENT",
            "short_description": "Test short description",
            "datetime": "2020-10-10",
            "comments": "Test Comments",
        },
        user=user,
    )
    assert form.is_valid() is False
    assert form.errors == {
        "type_descriptor": [
            "Select a valid choice. NOT ALLOWED EVENT is not one of the available choices."
        ]
    }


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
        "CAF_INITIAL_CAF_RECEIVED",
        "CAF_RECEIVED",
        "CAF_FEEDBACK_EMAILED_OES",
        "CAF_EMAILED_ROSA",
        "CAF_VALIDATION_SIGN_OFF",
        "CAF_VALIDATION_RECORD_EMAILED_TO_OES",
    ],
)
def test_allowable_caf_single_date_event_forms(allowed_type, user, caf):
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


@pytest.mark.parametrize(
    "allowed_type",
    ["CAF_INITIAL_CAF_RECEIVED", "CAF_VALIDATION_SIGN_OFF", "CAF_RECEIVED"],
)
def test_cannot_do_some_caf_single_date_events_on_same_day(allowed_type, user, caf):
    form1 = CAFSingleDateEventForm(
        {
            "type_descriptor": allowed_type,
            "related_caf": caf,
            "short_description": "Test Short Description",
            "date": "2010-07-01",
            "comments": "Meaningless comments",
        },
        user=user,
    )
    form2 = CAFSingleDateEventForm(
        {
            "type_descriptor": allowed_type,
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


def test_caf_twin_date_event(user, caf):
    form = CAFTwinDateEventForm(
        {
            "type_descriptor": "CAF_PEER_REVIEW_PERIOD",
            "related_caf": caf,
            "short_description": "Test Description",
            "start_date": "2009-10-01",
            "end_date": "2015-10-1",
            "comments": "Meaningless comments",
        },
        user=user,
    )
    assert form.is_valid()


@pytest.mark.parametrize("allowed_type", ["CAF_PEER_REVIEW_PERIOD", "CAF_VALIDATION_PERIOD"])
def test_cannot_create_twin_date_event_for_caf_whose_end_date_is_open(allowed_type, user, caf):
    e1 = CAFTwinDateEventForm(
        {
            "type_descriptor": allowed_type,
            "related_caf": caf,
            "short_description": "caf peer review for x company",
            "start_date": "2020-10-10",
            "comments": "nice comments for this event",
        },
        user=user,
    )
    e2 = CAFTwinDateEventForm(
        {
            "type_descriptor": allowed_type,
            "related_caf": caf,
            "short_description": "caf peer review for x company",
            "start_date": "2020-10-10",
            "comments": "nice comments for this event",
        },
        user=user,
    )
    assert e1.is_valid()
    e1.save()
    assert e2.is_valid() is False
    assert e2.errors == {
        "start_date": ["You cannot have two CAF events starting on the same date."]
    }


@pytest.mark.parametrize("allowed_type", ["CAF_PEER_REVIEW_PERIOD", "CAF_VALIDATION_PERIOD"])
def test_cannot_create_twin_date_event_where_end_date_precedes_start(allowed_type, user, caf):
    "This one is done with a database integrity check instead of a form validation"
    with pytest.raises(IntegrityError):
        CAFTwinDateEventForm(
            {
                "type_descriptor": allowed_type,
                "related_caf": caf,
                "short_description": "caf peer review for x company",
                "start_date": "2020-10-10",
                "end_date": "2020-10-09",
                "comments": "nice comments for this event",
            },
            user=user,
        ).save()
