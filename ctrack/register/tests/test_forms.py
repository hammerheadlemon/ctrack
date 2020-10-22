import pytest
from django.db import IntegrityError

from ..forms import CreateSimpleDateTimeEventForm, CAFSingleDateEventForm, CAFTwinDateEventForm, CreateNoteEventForm

pytestmark = pytest.mark.django_db


def test_init(user, org_with_people):
    """Here we test that we can pass in the user value from the view.
    We don't want that to be field in the form.
    """
    people_from_org = org_with_people.get_people()
    form = CreateSimpleDateTimeEventForm(
        {
            "type_descriptor": "MEETING",  # Must be Meeting as that is in the choices param
            "short_description": "Test short description",
            "date": "2010-10-10T13:00",
            "comments": "Test Comments",
            "location": "Transient Moats",
            "participants": people_from_org
        },
        user=user, org_slug=None
    )
    assert form.is_valid()


def test_simple_event_limited_to_org_participants(user, org, person):
    person.organisation = org
    person.save()
    people_from_org = org.get_people()
    form = CreateSimpleDateTimeEventForm(
        {
            "type_descriptor": "PHONE_CALL",
            "short_description": "Test Short Description",
            "date": "2010-10-10 10:00",
            "requested_response_date": "2020-12-24",
            "response_received_date": "2020-12-25",
            "participants": people_from_org,
            "url": "https://fake.url.com",
            "comments": "Test Comments not needed"
        }, user=user, org_slug=org.slug
    )
    assert form.is_valid()


def test_cannot_create_disallowed_single_date_event_type_with_form(user, org_with_people):
    form = CreateSimpleDateTimeEventForm(
        {
            "type_descriptor": "NOT ALLOWED EVENT",
            "short_description": "Test short description",
            "date": "2020-10-10",
            "comments": "Test Comments",
            "participants": org_with_people.get_people()
        },
        user=user, org_slug=None
    )
    assert form.is_valid() is False
    assert form.errors == {
        "type_descriptor": [
            "Select a valid choice. NOT ALLOWED EVENT is not one of the available choices."
        ]
    }


def test_create_simple_datetime_event(user, org_with_people):
    form = CreateSimpleDateTimeEventForm(
        {
            "type_descriptor": "PHONE_CALL",
            "short_description": "Test Short Description",
            "date": "2010-10-10 10:00",
            "requested_response_date": "2020-12-24",
            "response_received_date": "2020-12-25",
            "url": "https://fake.url.com",
            "comments": "Test Comments not needed",
            "participants": org_with_people.get_people()
        }, user=user, org_slug=None
    )
    assert form.is_valid()


def test_response_date_cannot_be_before_date(user, org_with_people):
    form = CreateSimpleDateTimeEventForm(
        {
            "type_descriptor": "PHONE_CALL",
            "short_description": "Test Short Description",
            "date": "2010-10-10 10:00",
            "requested_response_date": "2009-12-24",
            "response_received_date": None,
            "comments": "Test Comments not needed",
            "participants": org_with_people.get_people()
        }, user=user, org_slug=None
    )
    assert not form.is_valid()
    assert form.errors == {"__all__": ["Requested response cannot be before date."]}


def test_meeting_blank_data(user, org_with_people):
    """Missing datetime fields is required. Location is optional"""
    form = CreateSimpleDateTimeEventForm(
        {
            "type_descriptor": "MEETING",
            "short_description": "Test short description",
            "comments": "Test Comments",
            "participants": org_with_people.get_people()
        },
        user=user, org_slug=None
    )
    assert form.is_valid() is False
    assert form.errors == {"date": ["This field is required."]}


def test_create_note(user, org_with_people):
    """
    A note is related to an organisation rather than to persons in that organisation.
    """
    form = CreateNoteEventForm(
        {
            "type_descriptor": "NOTE",
            "short_description": "Test note",
            "organisation": org_with_people,
            "private": True,
            "url": "https://www.bobbins.com/there-bos"
        }, user=user
    )
    assert form.is_valid()


@pytest.mark.parametrize(
    "allowed_type",
    [
        "CAF_INITIAL_CAF_RECEIVED",
        "CAF_RECEIVED",
        "CAF_INITIAL_REVIEW_COMPLETE",
        "CAF_FEEDBACK_EMAILED_OES",
        "CAF_EMAILED_ROSA",
        "CAF_VALIDATION_SIGN_OFF",
        "CAF_VALIDATION_RECORD_EMAILED_TO_OES",
    ],
)
def test_caf_single_date_event_forms(allowed_type, user, caf):
    form = CAFSingleDateEventForm(
        {
            "type_descriptor": allowed_type,
            "related_caf": caf,
            "short_description": "Test Short Description",
            "date": "2010-07-01",
            "comments": "Meaningless comments",
        },
        user=user, caf_id=caf.id
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
        user=user, caf_id=caf.id
    )
    form2 = CAFSingleDateEventForm(
        {
            "type_descriptor": allowed_type,
            "related_caf": caf,
            "short_description": "Test Short Description",
            "date": "2010-07-01",
            "comments": "Meaningless comments",
        },
        user=user, caf_id=caf.id
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
        user=user, caf_id=caf.id
    )
    form2 = CAFSingleDateEventForm(
        {
            "type_descriptor": "CAF_EMAILED_ROSA",
            "related_caf": caf,
            "short_description": "Test Short Description 2",
            "date": "2010-07-01",
            "comments": "Meaningless comments 2",
        },
        user=user, caf_id=caf.id
    )
    assert form1.is_valid()
    assert form2.is_valid()


def test_caf_twin_date_event(user, caf):
    form = CAFTwinDateEventForm(
        {
            "type_descriptor": "CAF_PEER_REVIEW_PERIOD",
            "related_caf": caf,
            "short_description": "Test Description",
            "date": "2009-10-01",
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
            "date": "2020-10-10",
            "comments": "nice comments for this event",
        },
        user=user,
    )
    e2 = CAFTwinDateEventForm(
        {
            "type_descriptor": allowed_type,
            "related_caf": caf,
            "short_description": "caf peer review for x company",
            "date": "2020-10-10",
            "comments": "nice comments for this event",
        },
        user=user,
    )
    assert e1.is_valid()
    e1.save()
    assert e2.is_valid() is False
    assert e2.errors == {
        "date": ["You cannot have two CAF events starting on the same date."]
    }


@pytest.mark.parametrize("allowed_type", ["CAF_PEER_REVIEW_PERIOD", "CAF_VALIDATION_PERIOD"])
def test_cannot_create_twin_date_event_where_end_date_precedes_start(allowed_type, user, caf):
    """This one is done with a database integrity check instead of a form validation"""
    with pytest.raises(IntegrityError):
        CAFTwinDateEventForm(
            {
                "type_descriptor": allowed_type,
                "related_caf": caf,
                "short_description": "caf peer review for x company",
                "date": "2020-10-10",
                "end_date": "2020-10-09",
                "comments": "nice comments for this event",
            },
            user=user,
        ).save()
