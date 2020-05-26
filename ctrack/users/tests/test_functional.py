"""
Functional tests. Are probably SLOW thanks to using Selenium to load a browser instance.

The use case being tested here is related to a user being able to log in and hit
the correct page, containing their details. Those details depend on whether they are
a regular user or a stakeholder user.
"""

import time

import pytest

from ctrack.organisations.models import Stakeholder
from ctrack.users.models import User

pytestmark = pytest.mark.django_db


def test_user_can_log_in(browser, live_server):
    User.objects.create_user(username="toss", password="knob")
    browser.get(live_server + "/accounts/login")
    browser.find_element_by_id("id_login").send_keys("toss")
    browser.find_element_by_id("id_password").send_keys("knob")
    browser.find_element_by_id("sign_in_button").submit()
    time.sleep(1)
    current_url = browser.current_url
    assert current_url == live_server + "/users/toss/"


def test_profile_page_html(person, user, browser, live_server):
    stakeholder = Stakeholder.objects.create(person=person)
    user.stakeholder = stakeholder
    user.save()
    browser.get(live_server + f"/users/{user.username}/")
