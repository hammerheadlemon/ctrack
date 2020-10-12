import pytest

from ctrack.register.views import SingleDateTimeEventCreate

pytestmark = pytest.mark.django_db


class TestSingleDateFormView:
    def test_single_datetime_event_form(self, user, request_factory):
        view = SingleDateTimeEventCreate()
        request = request_factory.get("/register/event/create-single-datetime/")
        request.user = user
        view.request = request
        response = SingleDateTimeEventCreate.as_view()(request)
        assert response.status_code == 200
        assert not response.context_data["form"].is_bound
        for k in ["type_descriptor", "short_description", "datetime", "comments", "location"]:
            assert k in response.context_data["form"].fields
