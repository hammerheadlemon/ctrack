import pytest
from django.test import RequestFactory

from ctrack.organisations.models import AddressType
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
    address_type = AddressType.objects.create(descriptor="Random Type")
    return AddressFactory(type=address_type)


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()
