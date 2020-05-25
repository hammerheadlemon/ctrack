import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory

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


def test_profile_view_contains_organisation_information(person):
    """url: users/username
    This is where users are redirected to when they log in and where I want to capture
    information about the user - particularly if they are an OES user.
    """
    user = get_user_model().objects.create_user(
        username="testy", email="testy@test.com", password="test1020"
    )
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
    assert response.context_data["user"].username == "testy"
    assert response.context_data["user"].is_stakeholder() is True
    assert response.context_data["user"].stakeholder.person.first_name == "Chinaplate"

    # Two ways of getting the organisaton name
    assert (
        response.context_data["user"].stakeholder.person.get_organisation_name()
        == org_name
    )
    assert response.context_data["user"].get_organisation_name() == org_name
    assert response.context_data["user"].stakeholder.person.first_name == "Chinaplate"
