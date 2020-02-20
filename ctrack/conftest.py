import pytest
from django.test import RequestFactory

from ctrack.users.models import User
from ctrack.organisations.models import Organisation, Address
from ctrack.users.tests.factories import (
    UserFactory,
)
from ctrack.organisations.tests.factories import OrganisationFactory, AddressFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def org() -> Organisation:
    return OrganisationFactory()


@pytest.fixture
def addr() -> Address:
    return AddressFactory()


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()
