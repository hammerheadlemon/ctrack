import os

import pytest
from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from django.test import RequestFactory
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from ctrack.organisations.models import (
    Address,
    AddressType,
    Mode,
    Organisation,
    Stakeholder,
    Submode,
)
from ctrack.organisations.tests.factories import (
    AddressFactory,
    OrganisationFactory,
    PersonFactory,
    RoleFactory,
)
from ctrack.users.models import User
from ctrack.users.tests.factories import UserFactory


@pytest.fixture
def role():
    return RoleFactory.create(name="Test Role")


@pytest.fixture
def org_with_people(role):
    org = OrganisationFactory.create(
        submode=None,
        name="TEST ORGANISATION",
        designation_type=3,
        registered_company_name="Test PLC",
        comments="NA",
    )
    PersonFactory.create(
        role=role,
        job_title="Test Job Title",
        predecessor=None,
        organisation__submode=None,
        organisation=org,
    )
    return org


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def cct_user_group() -> Group:
    """
    TODO: An inspector will not require this many permissions! Reduce.
    """
    group = Group.objects.create(name="cct_user")
    ctrack_permissions = Permission.objects.filter(
        Q(codename__contains="address")
        | Q(codename__contains="addresstype")
        | Q(codename__contains="mode")
        | Q(codename__contains="organisation")
        | Q(codename__contains="role")
        | Q(codename__contains="submode")
        | Q(codename__contains="person")
        | Q(codename__contains="applicablesystem")
        | Q(codename__contains="caf")
        | Q(codename__contains="documentfile")
        | Q(codename__contains="filestore")
        | Q(codename__contains="grading")
        | Q(codename__contains="engagementtype")
        | Q(codename__contains="engagementevent")
        | Q(codename__contains="cafassessment")
        | Q(codename__contains="cafobjective")
        | Q(codename__contains="cafprinciple")
        | Q(codename__contains="cafcontributingoutcome")
        | Q(codename__contains="cafassessmentoutcomescore")
        | Q(codename__contains="achievmentlevel")
        | Q(codename__contains="igp")
        | Q(codename__contains="stakeholder")
        | Q(codename__contains="incidentreport")
    )
    group.permissions.add(*ctrack_permissions)
    return group


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def person(user):
    role = RoleFactory.create(name="Compliance Inspector")
    mode = Mode.objects.create(descriptor="Rail")
    submode = Submode.objects.create(descriptor="Light Rail", mode=mode)
    org = OrganisationFactory.create(submode=submode)
    person = PersonFactory.create(
        first_name="Toss",
        last_name="McBride",
        role=role,
        predecessor=None,
        organisation__submode=submode,
        organisation=org,
    )
    return person


@pytest.fixture
def org() -> Organisation:
    return OrganisationFactory()


@pytest.fixture
def addr() -> Address:
    address_type = AddressType.objects.create(descriptor="Random Type")
    return AddressFactory(type=address_type)


@pytest.fixture
def stakeholder_user(person):
    user = User.objects.create_user(username="toss", password="knob")
    stakeholder = Stakeholder.objects.create(person=person)
    user.stakeholder = stakeholder
    user.save()
    return user


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()


@pytest.fixture
def browser(request):
    "Provide selenium webdriver instance."
    os.environ["PATH"] += os.pathsep + os.getcwd()
    options = Options()
    options.headless = True
    browser_ = webdriver.Firefox(firefox_options=options)
    yield browser_
    browser_.quit()
