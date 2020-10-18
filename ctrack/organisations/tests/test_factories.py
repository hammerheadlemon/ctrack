import pytest

from ctrack.organisations.tests.factories import (
    OrganisationFactory,
    PersonFactory,
    RoleFactory, SingleDateTimeEventFactory,
)

pytestmark = pytest.mark.django_db


def test_organisation_factory():
    o = OrganisationFactory.build()
    assert o.name


def test_role_factory():
    r = RoleFactory.build()
    assert r.name


def test_person_factory():
    r = RoleFactory.build()
    p = PersonFactory.build(role=r, predecessor__predecessor=None)
    assert p.first_name


def test_meeting_event_factory():
    meeting = SingleDateTimeEventFactory.create(type_descriptor="MEETING")
    assert meeting.type_descriptor == "MEETING"
