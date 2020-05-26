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


def test_user_can_log_in(browser, person, live_server):

    # Toss McBride is an OES user. He logs into the system...
    stakeholder = Stakeholder.objects.create(person=person)

    user = User.objects.create_user(username="toss", password="knob")
    user.stakeholder = stakeholder
    user.save()
    browser.get(live_server + "/accounts/login")
    browser.find_element_by_id("id_login").send_keys("toss")
    browser.find_element_by_id("id_password").send_keys("knob")
    browser.find_element_by_id("sign_in_button").submit()
    time.sleep(1)
    current_url = browser.current_url
    assert current_url == live_server + "/"

    # On the other side, he sees some basic details about himself.
    assert "ctrack - Department for Transport" in browser.title

    # Such as his own name in an H1 tag!
    h1 = browser.find_element_by_tag_name("h1")
    assert h1.text == "Welcome to ctrack - Department for Transport"
