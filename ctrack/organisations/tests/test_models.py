import pytest
from slugify import slugify

from ctrack.organisations.models import Organisation

pytestmark = pytest.mark.django_db


def test_organisation_get_absolute_url(org):
    slug = slugify(org.name)
    assert org.get_absolute_url() == f"/organisations/{slug}/"


def test_delete_organisation(org_with_people):
    orgs = Organisation.objects.all()
    assert org_with_people in orgs
    Organisation.delete(org_with_people)
    # Assert that the record has been deleted
    assert Organisation.objects.count() == 0


def test_update_organisation(org_with_people):
    # Change the name of the organisation
    org_with_people.name = "Tonkers Ltd"
    org_with_people.save()
    assert org_with_people.name == "Tonkers Ltd"


def test_new_address(addr):
    # The address "has" an organisation
    assert addr.organisation.name


def test_incident_report(org_with_people):
    breakpoint()
    pass
