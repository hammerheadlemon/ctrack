import pytest
from slugify import slugify

from ctrack.organisations.models import IncidentReport, Organisation
from ctrack.caf.models import EssentialService

pytestmark = pytest.mark.django_db


def test_organisation_get_absolute_url(org):
    slug = slugify(org.name)
    assert org.get_absolute_url() == f"/organisations/{slug}/"


def test_update_organisation(org_with_people):
    # Change the name of the organisation
    org_with_people.name = "Tonkers Ltd"
    org_with_people.save()
    assert org_with_people.name == "Tonkers Ltd"


def test_new_address(addr):
    # The address "has" an organisation
    assert addr.organisation.name


def test_essential_service():
    es = EssentialService()
    assert es
