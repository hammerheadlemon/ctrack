import pytest
from django.test import RequestFactory

from ctrack.organisations.models import (
    Address,
    AddressType,
    Mode,
    Organisation,
    Submode,
)
from ctrack.organisations.tests.factories import (
    AddressFactory,
    OrganisationFactory,
    PersonFactory,
    RoleFactory,
)
from ctrack.users.models import User
from ctrack.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def person(user):
    role = RoleFactory.create(name="Compliance Inspector")
    mode = Mode.objects.create(descriptor="Rail")
    submode = Submode.objects.create(descriptor="Light Rail", mode=mode)
    org = OrganisationFactory.create(submode=submode)
    person = PersonFactory.create(
        role=role,
        updated_by=user,
        predecessor=None,
        organisation__submode=submode,
        organisation=org,
    )
    return person


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
