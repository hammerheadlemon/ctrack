import pytest
from django.test import TestCase
from django.urls import reverse

from ctrack.register.views import SingleDateTimeEventCreate

# Doing this allows us to use TestCase assertions (assertIn, etc)
test_case = TestCase("run")

pytestmark = pytest.mark.django_db


class TestSingleDateTimeEvent:
    def test_add_single_datetime_event_form(self, client):
        url = reverse("register:event_create_simple_event")
        response = client.get(url)
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

    @pytest.mark.parametrize("bad_date,expected_error", [
        ("NOT A DATE", "Enter a valid date/time."),
        ("202002-10-12", "Enter a valid date/time."),
        ("32 May 2020", "Enter a valid date/time."),
        ("May 2020", "Enter a valid date/time.")
    ])
    def test_bad_date(self, bad_date, expected_error, client):
        url = reverse("register:event_create_simple_event")
        data = {
            "type_descriptor": "MEETING",
            "short_description": "Test Short Description",
            "datetime": bad_date,
            "comments": "Blah...",
            "location": "The Moon",
        }
        response = client.post(url, data)
        assert response.status_code == 200
        html = response.content.decode("utf-8")
        test_case.assertIn(expected_error, html)

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
        url = reverse("register:event_create_simple_event")
        data = {
            "type_descriptor": bad_type,
            "short_description": "Test Short Description",
            "datetime": "2010-10-10",
            "comments": "Blah...",
            "location": "The Moon",
        }
        response = client.post(url, data)
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


class TestSingleDateCAFEventViews:
    def test_initial_caf_received(self, client):
        url = reverse("register:event_create_caf_single_date_event")
        response = client.get(url)
        assert response.status_code == 200
