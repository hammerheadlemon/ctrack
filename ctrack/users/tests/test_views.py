import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory

from ctrack.organisations.tests.factories import OrganisationFactory
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


def test_profile_view_contains_organisation_information():
    """url: users/username
    This is where users are redirected to when they log in and where I want to capture
    information about the user - particularly if they are an OES user.
    """
    org = OrganisationFactory.create()
    user = get_user_model().objects.create_user(
        username="testy",
        email="testy@test.com",
        password="test1020",
        oes_user=True,
        organisation=org,
    )
    factory = RequestFactory()
    request = factory.get(f"/users/{user.username}")
    # we have to do the following to simulate logged-in user
    # Django Advanced Testing Topics
    request.user = user
    response = UserDetailView.as_view()(request, username=user.username)
    assert response.status_code == 200
    assert response.context_data["object"].oes_user is True
    # TODO - work out how we can attach an organisation to the User model
    assert response.context_data["object"].organisation.name == org.name
