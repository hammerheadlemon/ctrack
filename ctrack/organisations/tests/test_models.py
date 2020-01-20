import pytest
from slugify import slugify

from ..models import Organisation

pytestmark = pytest.mark.django_db


def test_organisation_get_absolute_url(org: Organisation):
    slug = slugify(org.name)
    assert org.get_absolute_url() == f"/organisations/{slug}/"
