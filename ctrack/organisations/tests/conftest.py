# TODO Here we need to make use of the populate script to create a massive
#      test fixture.
import pytest

from ctrack.core.utils import populate_db
from ctrack.organisations.tests.factories import (
    OrganisationFactory,
    PersonFactory,
    RoleFactory,
)


@pytest.fixture
def role():
    return RoleFactory.create(name="Test Role")


@pytest.fixture
def org_with_people(role):
    org = OrganisationFactory.create(
        submode=None,
        name="TEST ORGANISATION",
        designation_type=3,
        registered_company_name="Test PLC",
        comments="NA",
    )
    PersonFactory.create(
        role=role,
        job_title="Test Job Title",
        predecessor=None,
        organisation__submode=None,
        organisation=org,
    )
    return org
