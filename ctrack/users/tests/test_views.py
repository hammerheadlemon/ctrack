import pytest
from django.test import RequestFactory

from ctrack.core.views import home_page
from ctrack.organisations.models import Stakeholder
from ctrack.users.models import User
from ctrack.users.views import UserDetailView, UserRedirectView, UserUpdateView

pytestmark = pytest.mark.django_db


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

        assert view.get_redirect_url() == f"/users/{user.username}/"


def test_profile_view_contains_organisation_information(person, user):
    """
    This tests the context_data - not the rendered page... We'll do that in the
    next test.
    """
    org_name = person.organisation.name
    stakeholder = Stakeholder.objects.create(person=person)
    user.stakeholder = stakeholder
    user.save()
    factory = RequestFactory()
    request = factory.get(f"/users/{user.username}")

    # we have to do the following to simulate logged-in user
    # Django Advanced Testing Topics
    request.user = user

    # We pass 'username' rather than 'slug' here because we are setting 'slug_url_kwarg' in our CBV.
    response = UserDetailView.as_view()(request, username=user.username)

    assert response.status_code == 200
    assert response.context_data["user"].username == user.username
    assert response.context_data["user"].is_stakeholder() is True
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
    assert response.content[:15] == b"<!DOCTYPE html>"
    assert b"<title>ctrack - Department for Transport</title>" in response.content
    assert b"<h1>Welcome to ctrack - Department for Transport</h1>" in response.content
    assert b"</html>" in response.content


def test_regular_user_redirected_to_their_template_on_login(django_user_model):
    """
    When a user logs in without a stakeholder mapping, they get sent to the regular user
    template.
    """
    user = django_user_model.objects.create_user(username="toss", password="knob")
    factory = RequestFactory()
    request = factory.get("/")
    request.user = user
    response = home_page(request)
    assert response.status_code == 200
    assert b"<p>THIS IS A TEMPLATE FOR A REGULAR USER</p>" in response.content


def test_stakeholder_redirected_to_their_template_on_login(django_user_model, person):
    """
    When a user logs in WITH a stakeholder mapping, they get sent to the stakehoder user
    template.
    """
    user = django_user_model.objects.create_user(username="toss", password="knob")
    stakeholder = Stakeholder.objects.create(person=person)
    user.stakeholder = stakeholder
    user.save()
    factory = RequestFactory()
    request = factory.get("/")
    request.user = user
    response = home_page(request)
    assert response.status_code == 200
    assert b"THIS IS A TEMPLATE FOR A STAKEHOLDER USER" in response.content
