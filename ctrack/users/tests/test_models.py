import pytest

from ctrack.organisations.models import Stakeholder

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user):
    assert user.get_absolute_url() == f"/users/{user.username}/"


def test_user_is_person_object(user):

    """User comes from ctrack.conftest.
    """
    assert user


def test_stakeholder_model(person):
    """
    A stakeholder is someone who is part of the regime but also has user access to the
    the system.
    """
    stakeholder = Stakeholder(person=person)
    assert stakeholder
