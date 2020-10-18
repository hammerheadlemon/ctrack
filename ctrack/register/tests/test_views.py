import pytest
from django.test import TestCase
from django.urls import reverse

from ctrack.register.views import SingleDateTimeEventCreate

# Doing this allows us to use TestCase assertions (assertIn, etc)
test_case = TestCase("run")

pytestmark = pytest.mark.django_db


class TestSingleDateTimeEvent:
    url = reverse("register:event_create_simple_event")

    def test_add_single_datetime_event_form(self, client):
        response = client.get(self.url)
        assert response.status_code == 200

        form = response.context_data["form"]
        assert not form.is_bound
        expected_fields = [
            "type_descriptor",
            "short_description",
            "datetime",
            "comments",
            "location",
        ]
        for field in expected_fields:
            assert field in form.fields
        # We're keeping the use field out of the form
        assert "user" not in form.fields

    @pytest.mark.parametrize(
        "bad_date,expected_error",
        [
            ("NOT A DATE", "Enter a valid date/time."),
            ("202002-10-12", "Enter a valid date/time."),
            ("32 May 2020", "Enter a valid date/time."),
            ("May 2020", "Enter a valid date/time."),
        ],
    )
    def test_bad_date(self, bad_date, cct_user, expected_error, client):
        data = {
            "type_descriptor": "MEETING",
            "short_description": "Test Short Description",
            "datetime": bad_date,
            "comments": "Blah...",
            "location": "The Moon",
        }
        # we need to use the cct_user fixture here who has permissions
        # on the redirect page
        client.force_login(cct_user)
        response = client.post(self.url, data)
        assert response.status_code == 200
        html = response.content.decode("utf-8")
        test_case.assertIn(expected_error, html)

    @pytest.mark.parametrize("good_date", ["2010-10-10"])
    def test_good_date(self, good_date, cct_user, client):
        data = {
            "type_descriptor": "PHONE_CALL",
            "short_description": "Test Short Description",
            "datetime": good_date,
            "comments": "Blah...",
            "location": "The Moon",
        }
        client.force_login(cct_user)
        response = client.post(self.url, data, follow=True)
        test_case.assertRedirects(
            response,
            reverse("organisations:list"),
        )

    @pytest.mark.parametrize(
        "bad_type,expected_error",
        [
            (
                "Meeting X",
                "Select a valid choice. Meeting X is not one of the available choices.",
            ),
            (
                "Meeting Bunting Radgehead",
                "Select a valid choice. Meeting Bunting Radgehead is not one of the available choices.",
            ),
        ],
    )
    def test_add_incorrect_form_data_single_datetime(
        self, bad_type, expected_error, client
    ):
        data = {
            "type_descriptor": bad_type,
            "short_description": "Test Short Description",
            "datetime": "2010-10-10",
            "comments": "Blah...",
            "location": "The Moon",
        }
        response = client.post(self.url, data)
        assert response.status_code == 200
        html = response.content.decode("utf-8")
        test_case.assertIn(expected_error, html)

    def test_user_passed_as_kwarg(self, user, request_factory):
        view = SingleDateTimeEventCreate()
        request = request_factory.get("/register/event/create-simple-event/")
        request.user = user
        view.request = request
        view.setup(request)
        assert "user" in view.get_form_kwargs()

    def test_create_simple_event_without_org_means_no_participants(self, user, client):
        client.force_login(user)
        url = reverse("register:event_create_simple_event")
        response = client.get(url)
        html = response.content.decode("utf-8")
        assert '<input type="hidden" name="participants" id="id_participants">' in html

    def test_can_create_simple_event_with_org_slug(self, user, org, client):
        slug = org.slug
        url = reverse("register:event_create_simple_event_from_org", args=[slug])
        client.force_login(user)
        response = client.get(url)
        html = response.content.decode("utf-8")
        assert response.status_code == 200
        test_case.assertInHTML(f"Create a new simple event involving {org.name}", html)

    def test_org_passed_as_kwarg(self, user, org, request_factory):
        slug = org.slug
        view = SingleDateTimeEventCreate()
        url = reverse("register:event_create_simple_event_from_org", args=[slug])
        request = request_factory.get(url)
        request.user = user
        view.request = request
        view.setup(request)
        assert "org_slug" in view.get_form_kwargs()

    def test_meeting_type_and_org_passed_as_kwarg(
        self, user, org, request_factory
    ):
        event_type = "PHONE_CALL"
        slug = org.slug
        view = SingleDateTimeEventCreate()
        url = reverse("register:event_create_simple_event_from_org_with_type", args=[slug, event_type])
        request = request_factory.get(url)
        request.user = user
        view.request = request
        view.setup(request)
        assert "event_type" in view.get_form_kwargs()


class TestSingleDateCAFEventViews:
    def test_initial_caf_received(self, client):
        url = reverse("register:event_create_simple_event")
        response = client.get(url)
        assert response.status_code == 200
