import pytest
from django.contrib.auth import get_user_model
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
    request = factory.get("/organisations")
    request.user = user
    response = OrganisationListView.as_view()(request)
    assert response.status_code == 200
    assert len(response.context_data["organisation_list"]) == 3


def test_incident_report_create_view():
    user = get_user_model().objects.create_user(
        username="testy", email="testy@test.com", password="test1020"
    )
    org = OrganisationFactory.create()
    factory = RequestFactory()
    request = factory.get(f"{org.name}/create-incident-report")
    request.user = user
    response = IncidentReportCreateView.as_view()(request, org.slug)
    assert response.status_code == 200
