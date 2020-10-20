import pytest

from ctrack.organisations.models import Organisation, Submode, Mode
from ctrack.organisations.utils import inspectors_for_each_mode
from ctrack.organisations.tests.factories import OrganisationFactory

pytestmark = pytest.mark.django_db


def test_group_lead_inspector_by_submode(
    submode, mode, org, org_with_people, inspector1, inspector2
):
    # because I can't be bothered making another fixture
    submode1 = submode  # this is Light Rail by the way
    submode2 = Submode.objects.create(
        descriptor="Metro Rail", mode=Mode.objects.create(descriptor="Rail"))

    OrganisationFactory(submode=submode1, lead_inspector=inspector1, deputy_lead_inspector=inspector2)
    OrganisationFactory(submode=submode1, lead_inspector=inspector1, deputy_lead_inspector=inspector2)
    OrganisationFactory(submode=submode1, lead_inspector=inspector1, deputy_lead_inspector=inspector2)
    OrganisationFactory(submode=submode1, lead_inspector=inspector1, deputy_lead_inspector=inspector2)

    OrganisationFactory(submode=submode2, lead_inspector=inspector2, deputy_lead_inspector=inspector1)
    OrganisationFactory(submode=submode2, lead_inspector=inspector2, deputy_lead_inspector=inspector1)
    OrganisationFactory(submode=submode2, lead_inspector=inspector2, deputy_lead_inspector=inspector1)
    OrganisationFactory(submode=submode2, lead_inspector=inspector2, deputy_lead_inspector=inspector1)

    # We have two lead inspectors for submode1!
    org8 = OrganisationFactory(submode=submode1, lead_inspector=inspector2, deputy_lead_inspector=inspector1)

    orgs = Organisation.objects.filter(submode=submode)
    leads = [org.lead_inspector for org in orgs]
    for lead in leads[:3]:
        assert lead.first_name == "Cyril"

    for lead in leads[4:]:
        assert lead.first_name == "Ogilvie"

    lead_inspectors = inspectors_for_each_mode(lead_type="lead_inspector")
    deputy_lead_inspectors = inspectors_for_each_mode(lead_type="deputy_lead_inspector")
    assert lead_inspectors["Light Rail"] == {inspector1, inspector2}
    assert lead_inspectors["Metro Rail"] == {inspector2}
    assert deputy_lead_inspectors["Light Rail"] == {inspector2, inspector1}
    assert deputy_lead_inspectors["Metro Rail"] == {inspector1}
