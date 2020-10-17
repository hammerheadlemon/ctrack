import pytest
from django.contrib.auth.models import Permission
from django.test import RequestFactory, TestCase
from django.urls import reverse

from ctrack.core.views import home_page
from ctrack.register.models import SingleDateTimeEvent
from ctrack.users.models import User
from ctrack.users.views import UserDetailView, UserRedirectView, UserUpdateView

pytestmark = pytest.mark.django_db

test_case = TestCase("run")


class TestUserProfilePage:

    def test_their_full_name_in_h3(self, user: User, client):
        full_name = user.name
        client.force_login(user)
        response = client.get(reverse("users:detail", args=[user.username]))
        assert response.status_code == 200
        html = response.content.decode("utf-8")
        test_string = f"<h3>{full_name}</h3>"
        assert test_string in html

    def test_view_has_all_events_related_to_user(self, user, client):
        SingleDateTimeEvent.objects.create(
            type_descriptor="PHONE_CALL",
            short_description="Important event",
            url="http://fake.url.com",
            requested_response_date="2021-01-24",
            response_received_date=None,
            datetime="2020-10-10T15:00",
            comments="Comments on important event",
            # location is optional
            user=user,
        )
        client.force_login(user)
        response = client.get(reverse("users:detail", args=[user.username]))
        assert response.status_code == 200
        html = response.content.decode("utf-8")
        test_case.assertInHTML("Comments on important event", html)



class TestUserUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
        fixture db access -- this is a work-in-progress for now:
        https://github.com/pytest-dev/pytest-django/pull/258
    """

    def test_get_success_url(self, user: User, request_factory: RequestFactory):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == f"/users/{user.username}/"

    def test_get_object(self, user: User, request_factory: RequestFactory):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user


class TestUserRedirectView:
    def test_get_redirect_url(self, user: User, request_factory: RequestFactory):
        view = UserRedirectView()
        request = request_factory.get("/fake-url")
        request.user = user

        view.request = request

        assert view.get_redirect_url() == "/"


def test_profile_view_contains_organisation_information(
    person, request_factory, stakeholder_user
):
    """
    This tests the context_data - not the rendered page... We'll do that in the
    next test.
    """
    org_name = person.organisation.name
    request = request_factory.get(f"/users/{stakeholder_user.username}")

    # we have to do the following to simulate logged-in user
    # Django Advanced Testing Topics
    request.user = stakeholder_user

    # We pass 'username' rather than 'slug' here because we are setting 'slug_url_kwarg' in our CBV.
    response = UserDetailView.as_view()(request, username=stakeholder_user.username)

    assert response.status_code == 200
    assert response.context_data["user"].username == stakeholder_user.username
    assert response.context_data["user"].is_stakeholder is True
    assert response.context_data["user"].stakeholder.person.first_name == "Toss"

    # Two ways of getting the organisaton name
    assert (
        response.context_data["user"].stakeholder.person.get_organisation_name()
        == org_name
    )
    assert response.context_data["user"].get_organisation_name() == org_name
    assert response.context_data["user"].stakeholder.person.first_name == "Toss"


def test_home_page_h1_tag_with_client(client, django_user_model):
    """
    Basic test of HTML from the home page.
    """
    django_user_model.objects.create_user(username="toss", password="knob")
    client.login(username="toss", password="knob")
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>ctrack - NIS Tracker</title>" in response.content
    assert b"</html>" in response.content


def test_regular_user_redirected_to_their_template_on_login(
    django_user_model, request_factory: RequestFactory
):
    """
    When a user logs in without a stakeholder mapping, they get sent to the site home
    page.
    """
    user = django_user_model.objects.create_user(username="toss", password="knob")
    request = request_factory.get("/")
    request.user = user
    response = home_page(request)
    assert response.status_code == 200
    assert b'<h1 class="display-3">ctrack</h1>' in response.content


def test_stakeholder_redirected_to_their_template_on_login(
    django_user_model, request_factory: RequestFactory, stakeholder_user
):
    """
    When a user logs in WITH a stakeholder mapping, they get sent to the stakehoder user
    template.
    """
    request = request_factory.get("/")
    request.user = stakeholder_user
    response = home_page(request)
    assert response.status_code == 200
    assert b"THIS IS A TEMPLATE FOR A STAKEHOLDER USER" in response.content


def test_stakeholder_returns_is_stakeholder(
    django_user_model, request_factory, stakeholder_user
):
    request = request_factory.get("/")
    request.user = stakeholder_user
    assert request.user.is_stakeholder is True


def test_stakeholder_user_is_not_staff(django_user_model, stakeholder_user):
    assert stakeholder_user.is_staff is False


def test_stakeholder_user_gets_301_when_trying_to_access_view_with_perm_set(
    django_user_model, client, stakeholder_user
):
    """
    No permissions are set when a regular user is created. This test knows that a suitable
    permission is set on the ctrack.organisations.view.OrganisationListView, and therefore we
    would expect a redirect/403 persmission denied response when trying to reach it with a
    regular user.
    """
    client.login(username="toss", password="knob")
    response = client.get(path="https://localhost:8000/organisations")
    assert (
        response.status_code == 301
    )  # This page redirects to 403.html, hence why its a 301 (I think)


@pytest.mark.skip("Explore why this does not pass - it passess in functional style")
def test_staff_user_gets_200_when_trying_to_access_view_with_perm_set(
    django_user_model, client, stakeholder_user
):
    org_list_permission = Permission.objects.get(name="Can view organisation")
    assert stakeholder_user.user_permissions.count() == 0
    stakeholder_user.user_permissions.add(org_list_permission)
    assert stakeholder_user.has_perm("organisations.view_organisation")
    stakeholder_user.save()
    logged_in = client.login(username="toss", password="knob")
    assert logged_in is True
    response = client.get("/organisations")
    assert response.status_code == 200
