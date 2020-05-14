import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory

from ..views import OrganisationListView

pytestmark = pytest.mark.django_db


# https://docs.djangoproject.com/en/3.0/topics/testing/advanced/#example
def test_organisation_list_view(full_db_fixture):
    factory = RequestFactory()
    user = get_user_model().objects.create_user(
        username="testy", email="testy@test.com", password="test1020"
    )
    request = factory.get("/organisations")
    request.user = user
    response = OrganisationListView.as_view()(request)
    assert response.status_code == 200
    assert len(response.context_data["organisation_list"]) == 3
