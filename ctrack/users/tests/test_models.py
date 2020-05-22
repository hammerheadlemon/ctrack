import pytest
from django.contrib.auth import get_user_model

from ctrack.organisations.models import Mode, Person, Submode
from ctrack.organisations.tests.factories import (
    OrganisationFactory,
    PersonFactory,
    RoleFactory,
)
from ctrack.users.models import User

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


def test_user_is_person_object(user: User):
    """User comes from ctrack.conftest.
    """
    assert user.oes_user is False
