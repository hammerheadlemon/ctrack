import pytest
from slugify import slugify

from ..models import Organisation, Address

pytestmark = pytest.mark.django_db


def test_organisation_get_absolute_url(org: Organisation):
    slug = slugify(org.name)
    assert org.get_absolute_url() == f"/organisations/{slug}/"


def test_create_organisation(addr: Address):
    Organisation(name="Big Bad OES Corporation", address=addr).save()
    assert Organisation.objects.get(name="Big Bad OES Corporation")
    assert Organisation.objects.get(name="Big Bad OES Corporation").address.type.descriptor == "Primary Address"
