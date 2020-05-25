import pytest

from ctrack.organisations.models import Stakeholder

pytestmark = pytest.mark.django_db


def test_profile_page_html(person, user, browser):
    stakeholder = Stakeholder.objects.create(person=person)
    user.stakeholder = stakeholder
    user.save()
    browser.get(f"http://localhost:8000/users/{user.username}")
