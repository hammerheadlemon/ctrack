import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import RequestFactory
from django.urls import reverse

from ctrack.caf.tests.factories import PersonFactory
from ctrack.organisations.models import Mode, Submode
from ctrack.organisations.tests.factories import OrganisationFactory, RoleFactory
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


def test_only_member_of_cct_user_group_can_view_org_list():

    OrganisationFactory.create()
    OrganisationFactory.create()
    OrganisationFactory.create()

    group = Group.objects.create(name="cct_user")

    factory = RequestFactory()
    user = get_user_model().objects.create_user(
        username="testy", email="testy@test.com", password="test1020"
    )
    user.groups.add(group)
    org_list_permission = Permission.objects.get(name="Can view organisation")
    group.permissions.add(org_list_permission)
    # They get this permisson via the cct_user group
    assert user.has_perm("organisations.view_organisation")


def test_incident_report_create_view(stakeholder_user):
    org = OrganisationFactory.create()
    factory = RequestFactory()
    request = factory.get(f"{org.name}/create-incident-report")
    request.user = stakeholder_user
    response = IncidentReportCreateView.as_view()(request, org.slug)
    assert response.status_code == 200


def test_only_member_of_cct_user_group_can_view_a_single_person(
    stakeholder_user, org_with_people, client
):
    role = RoleFactory.create()
    submode = Submode.objects.create(
        descriptor="Light Rail", mode=Mode.objects.create(descriptor="Rail")
    )
    PersonFactory.create(
        role=role,
        predecessor=None,
        organisation__submode=submode,
        organisation=org_with_people,
    )
    PersonFactory.create(
        role=role,
        predecessor=None,
        organisation__submode=submode,
        organisation=org_with_people,
    )
    group = Group.objects.create(name="cct_user")

    stakeholder_user.groups.add(group)

    person_list_permission = Permission.objects.get(name="Can view person")
    group.permissions.add(person_list_permission)

    client.force_login(stakeholder_user)

    response = client.get(reverse("organisations:people"))

    # They get this permisson via the cct_user group
    assert stakeholder_user.has_perm("organisations.view_person")
    assert response.status_code == 200
