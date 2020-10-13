import pytest
from django.urls import reverse
from django.test import TestCase

test_case = TestCase("run")

from ctrack.register.views import SingleDateTimeEventCreate

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

    def test_add_incorrect_form_data_single_datetime(self, client):
        url = reverse("register:event_create_simple_event")
        data = {
            "type_descriptor": "Meeting X",
            "short_description": "Test Short Description",
            "datetime": "2010-10-10",
            "comments": "Blah...",
            "location": "The Moon"
        }
        response = client.post(url, data)
        assert response.status_code == 200
        html = response.content.decode("utf-8")
        test_case.assertIn("Select a valid choice. Meeting X is not one of the available choices.", html)


    def test_user_passed_as_kwarg(self, user, request_factory):
        view = SingleDateTimeEventCreate()
        request = request_factory.get("/register/event/create-simple-event/")
        request.user = user
        view.request = request
        view.setup(request)
        assert "user" in view.get_form_kwargs()

class TestSingleDateCAFEventViews:

    def test_initial_caf_recevied(self, client):
        pass

