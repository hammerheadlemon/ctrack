import pytest
from django.urls import reverse

from ctrack.register.views import SingleDateTimeEventCreate

pytestmark = pytest.mark.django_db


class TestMeetingEventFormView:

    def test_add_meeting_form(self, client):
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

    def test_user_passed_as_kwarg(self, user, request_factory):
        view = SingleDateTimeEventCreate()
        request = request_factory.get("/register/event/create-simple-event/")
        request.user = user
        view.request = request
        view.setup(request)
        assert "user" in view.get_form_kwargs()
