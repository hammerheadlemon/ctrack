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
from ctrack.organisations.views import IncidentReportCreateView, OrganisationDetailView
from ..utils import filter_private_events
from ..views import OrganisationListView

pytestmark = pytest.mark.django_db


def test_organisation_by_inspector_view(inspector1, inspector2, client, submode):
    org = OrganisationFactory(submode=submode, lead_inspector=inspector1, deputy_lead_inspector=inspector2)
    client.force_login(inspector1)
    response = client.get(reverse("organisations:list_by_inspector", args=[inspector1.id]))
    assert response.status_code == 200


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



def test_private_event_filter(user, org_with_people):
    """
    In this test we are creating five events, using two different users.
    Each event will be set to either private or not private. We are testing
    a function that will only allow private notes belonging to the logged in,
    or request.user user to be added to the view context. The context is not
    referred to here - only the utility function under test. The output from
    that filter function will go forward into the view context.
    """
    person = org_with_people.person_set.first()
    e1_user = SingleDateTimeEventFactory(
        type_descriptor="MEETING",
        short_description="First Event with user",
        private=True,
        user=user,
    )
    e2_user = SingleDateTimeEventFactory(
        type_descriptor="MEETING",
        short_description="Second Event with user",
        private=False,
        user=user,
    )
    e3_user = SingleDateTimeEventFactory(
        type_descriptor="MEETING",
        short_description="Third Event with user",
        private=True,
        user=user,
    )
    e1_user.participants.add(person)
    e1_user.save()
    e2_user.participants.add(person)
    e2_user.save()
    e3_user.participants.add(person)
    e3_user.save()
    user2 = get_user_model().objects.create(username="sam", email="asd@asdsd.com", password="123")
    e1_user2 = SingleDateTimeEventFactory(
        type_descriptor="MEETING",
        short_description="First Event with user2",
        private=False,
        user=user2,
    )
    e2_user2 = SingleDateTimeEventFactory(
        type_descriptor="MEETING",
        short_description="Second Event with user2",
        private=True,
        user=user2,
    )
    e1_user2.participants.add(person)
    e1_user2.save()
    e2_user2.participants.add(person)
    e2_user2.save()
    # This user needs permission to access the list view
    org_list_permission = Permission.objects.get(name="Can view organisation")
    assert user.user_permissions.count() == 0
    user.user_permissions.add(org_list_permission)
    assert user.has_perm("organisations.view_organisation")
    user.save()
    factory = RequestFactory()
    request = factory.get(reverse("organisations:detail", args=[org_with_people.slug]))
    request.user = user
    response = OrganisationDetailView.as_view()(request, slug=org_with_people.slug)
    assert response.status_code == 200
    events = person.get_single_datetime_events()
    assert events.count() == 5
    assert len(filter_private_events(events, user2)) == 3


def test_logged_in_user_can_only_see_their_private_events(
    user, org_with_people, client
):
    org_list_permission = Permission.objects.get(name="Can view organisation")
    assert user.user_permissions.count() == 0
    user.user_permissions.add(org_list_permission)
    assert user.has_perm("organisations.view_organisation")
    user.save()
    person = org_with_people.person_set.first()

    # This user creates three events
    e1 = SingleDateTimeEventFactory(
        type_descriptor="MEETING",
        short_description="First Event",
        private=True,
        user=user,
    )
    e2 = SingleDateTimeEventFactory(
        type_descriptor="MEETING",
        short_description="Second Event",
        private=False,
        user=user,
    )
    e3 = SingleDateTimeEventFactory(
        type_descriptor="MEETING",
        short_description="Third Event",
        private=True,
        user=user,
    )
    e1.participants.add(person)
    e1.save()
    e2.participants.add(person)
    e2.save()
    e3.participants.add(person)
    e3.save()
    response = client.get(
        reverse("organisations:detail", kwargs={"slug": org_with_people.slug})
    )
    assert response.status_code == 200
    html = response.content.decode("utf-8")
    assert "First Event" in html
    assert "Second Event" in html
    assert "Third Event" in html
    assert "PRIVATE" in html

    # A second user adds events based on this person/organisation
    user2 = get_user_model().objects.create(
        username="bobbins", email="bobbins@gog.com", password="bobbins123345"
    )
    user2.user_permissions.add(org_list_permission)
    assert user2.has_perm("organisations.view_organisation")
    user2.save()
    client.logout()
    client.force_login(user2)
    response2 = client.get(
        reverse("organisations:detail", kwargs={"slug": org_with_people.slug})
    )
    html2 = response2.content.decode("utf-8")
    assert response2.status_code == 200
    # They should not be able to see First Event which was created by another
    # user and marked private.
    assert "First Event" not in html2
    assert "Second Event" in html2
    assert "Third Event" not in html2


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
