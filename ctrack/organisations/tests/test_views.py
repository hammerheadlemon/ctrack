import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import RequestFactory
from django.urls import reverse

from ctrack.caf.tests.factories import PersonFactory
from ctrack.organisations.tests.factories import (
    OrganisationFactory,
    SingleDateTimeEventFactory,
)
from ctrack.organisations.views import IncidentReportCreateView

from ..views import OrganisationListView

pytestmark = pytest.mark.django_db


def test_meetings_in_organisation_detail_view(user, client, org_with_people):
    org_list_permission = Permission.objects.get(name="Can view organisation")
    assert user.user_permissions.count() == 0
    user.user_permissions.add(org_list_permission)
    assert user.has_perm("organisations.view_organisation")
    user.save()
    person = org_with_people.person_set.first()
    e1 = SingleDateTimeEventFactory.create(
        type_descriptor="MEETING", short_description="First Meeting"
    )
    e2 = SingleDateTimeEventFactory.create(
        type_descriptor="MEETING", short_description="Second Meeting"
    )
    e1.participants.add(person)
    e1.save()
    e2.participants.add(person)
    e2.save()
    client.force_login(user)
    response = client.get(
        reverse("organisations:detail", kwargs={"slug": org_with_people.slug})
    )
    assert response.status_code == 200
    html = response.content.decode("utf-8")
    assert "First Meeting" in html


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
    stakeholder_user, org_with_people, client, role, submode
):
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
