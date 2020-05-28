"""
Functional tests. Are probably SLOW thanks to using Selenium to load a browser instance.

The use case being tested here is related to a user being able to log in and hit
the correct page, containing their details. Those details depend on whether they are
a regular user or a stakeholder user.
"""

import time

import pytest
from django.contrib.auth.models import Permission

from ctrack.users.models import User

pytestmark = pytest.mark.django_db


def test_regular_user_can_log_in(browser, live_server):

    # Toss McBride is an OES user. He logs into the system...
    User.objects.create_user(username="toss", password="knob")
    browser.get(live_server + "/accounts/login")
    browser.find_element_by_id("id_login").send_keys("toss")
    browser.find_element_by_id("id_password").send_keys("knob")
    browser.find_element_by_id("sign_in_button").submit()
    time.sleep(1)
    current_url = browser.current_url
    assert current_url == live_server + "/"

    type_user_message = browser.find_elements_by_tag_name("p")
    assert "THIS IS A TEMPLATE FOR A REGULAR USER" in [
        m.text for m in type_user_message
    ]


def test_stakeholder_can_log_in_and_see_their_home(browser, live_server, stakeholder):
    # Toss McBride is an OES user. He logs into the system...

    user = User.objects.create_user(username="toss", password="knob")
    user.stakeholder = stakeholder
    org = user.stakeholder.person.get_organisation_name()
    user.save()
    browser.get(live_server + "/accounts/login")
    browser.find_element_by_id("id_login").send_keys("toss")
    browser.find_element_by_id("id_password").send_keys("knob")
    browser.find_element_by_id("sign_in_button").submit()
    time.sleep(1)
    current_url = browser.current_url
    assert current_url == live_server + "/"

    p_tags = browser.find_elements_by_tag_name("p")
    h2_tags = browser.find_elements_by_tag_name("h2")
    assert "THIS IS A TEMPLATE FOR A STAKEHOLDER USER" in [m.text for m in p_tags]
    assert org in [m.text for m in h2_tags]
    assert (
        f"{user.stakeholder.person.first_name} {user.stakeholder.person.last_name}"
        in [m.text for m in p_tags]
    )


def test_stakeholder_can_log_in_but_receieved_permisson_denied_when_off_piste(
    browser, live_server, stakeholder
):
    user = User.objects.create_user(username="toss", password="knob")
    user.stakeholder = stakeholder
    user.save()
    browser.get(live_server + "/accounts/login")
    browser.find_element_by_id("id_login").send_keys("toss")
    browser.find_element_by_id("id_password").send_keys("knob")
    browser.find_element_by_id("sign_in_button").submit()
    time.sleep(1)
    # Try to browser to Organisations list
    browser.get(live_server + "/organisations")
    assert "Sorry. You do not have permission to view this page." in [
        x.text for x in browser.find_elements_by_tag_name("p")
    ]


def test_stakeholder_user_with_permissions_can_view_page(
    browser, live_server, stakeholder
):
    user = User.objects.create_user(username="toss", password="knob")
    user.stakeholder = stakeholder
    org_list_permission = Permission.objects.get(name="Can view organisation")

    # Add the permission to view an Organisation, which is set on OrganisationListView
    assert user.user_permissions.count() == 0
    user.user_permissions.add(org_list_permission)
    assert user.user_permissions.count() == 1
    user.save()

    browser.get(live_server + "/accounts/login")
    browser.find_element_by_id("id_login").send_keys("toss")
    browser.find_element_by_id("id_password").send_keys("knob")
    browser.find_element_by_id("sign_in_button").submit()
    time.sleep(1)
    # Try to browser to Organisations list
    browser.get(live_server + "/organisations")
    assert "Organisations" in browser.title


def test_stakeholder_user_can_see_requisite_subtitles_on_home_page(
    browser, live_server, stakeholder
):
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

    h2 = browser.find_elements_by_tag_name("h2")
    assert "Incident Reporting" in [x.text for x in h2]
    assert "Audits and Inspections" in [x.text for x in h2]
    assert "NIS systems" in [x.text for x in h2]
    assert "DfT Engagement" in [x.text for x in h2]


def test_stakeholder_logs_into_system_and_submits_incident_form(
    browser, live_server, stakeholder
):
    user = User.objects.create_user(username="toss", password="knob")
    user.stakeholder = stakeholder
    user.save()
    browser.get(live_server + "/accounts/login")
    browser.find_element_by_id("id_login").send_keys("toss")
    browser.find_element_by_id("id_password").send_keys("knob")
    browser.find_element_by_id("sign_in_button").submit()
    time.sleep(1)
    current_url = browser.current_url
    browser.get(current_url)

    # Clicks the Report a NIS incident button
    browser.find_element_by_id("id_submit_incident_button").submit()

    # Gets to the correct page
    assert "Submit a new NIS Incident Report to DfT" in browser.title

    # The name of her organisation is already there in the first field
    assert (
        browser.find_element_by_id("id_org_field").text
        == user.stakeholder.person.get_organisation_name()
    )

    # Her name is already in the "Name of person reporting field"
    assert (
        browser.find_element_by_id("id_person_reporting_field").text
        == user.stakeholder.person
    )

    # Her role is already in the "Role" field
    assert browser.find_element_by_id("id_role_field").text == user.stakeholder.role

    # Her phone number is already in the "Phone Number" field
    assert (
        browser.find_element_by_id("id_phone_number_field").text
        == user.stakeholder.mobile
    )
    assert pytest.fail("WE GO NO FURTHER")
