import pytest
from slugify import slugify

from ..models import Organisation, Address

pytestmark = pytest.mark.django_db


def test_organisation_get_absolute_url(org: Organisation):
    slug = slugify(org.name)
    assert org.get_absolute_url() == f"/organisations/{slug}/"


def test_create_organisation():
    Organisation(name="Big Bad OES Corporation").save()
    # The organisation is saved in the db
    assert Organisation.objects.get(name="Big Bad OES Corporation")


def test_delete_organisation(org: Organisation):
    orgs = Organisation.objects.all()
    assert org in orgs
    Organisation.delete(org)
    # Assert that the record has been deleted
    assert Organisation.objects.count() == 0


def test_update_organisation(org: Organisation):
    # Change the name of the organisation
    org.name = "Tonkers Ltd"
    org.save()
    assert org.name == "Tonkers Ltd"


def test_new_address(addr: Address):
    # The address "has" an organisation
    assert addr.organisation.name
