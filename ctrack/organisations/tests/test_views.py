import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import RequestFactory

from ctrack.organisations.tests.factories import OrganisationFactory
from ctrack.organisations.views import IncidentReportCreateView

from ..views import OrganisationListView

pytestmark = pytest.mark.django_db


# https://docs.djangoproject.com/en/3.0/topics/testing/advanced/#example
def test_organisation_list_view():

    OrganisationFactory.create()
    OrganisationFactory.create()
    OrganisationFactory.create()

    factory = RequestFactory()
    user = get_user_model().objects.create_user(
        username="testy", email="testy@test.com", password="test1020"
    )
    # This user needs permission to acccess the list view
    org_list_permission = Permission.objects.get(name="Can view organisation")
    assert user.user_permissions.count() == 0
    user.user_permissions.add(org_list_permission)
    assert user.has_perm("organisations.view_organisation")
    user.save()
    request = factory.get("/organisations")
    request.user = user
    response = OrganisationListView.as_view()(request)
    assert response.status_code == 200
    assert len(response.context_data["organisation_list"]) == 3


def test_incident_report_create_view(stakeholder_user):
    org = OrganisationFactory.create()
    factory = RequestFactory()
    request = factory.get(f"{org.name}/create-incident-report")
    request.user = stakeholder_user
    response = IncidentReportCreateView.as_view()(request, org.slug)
    assert response.status_code == 200
