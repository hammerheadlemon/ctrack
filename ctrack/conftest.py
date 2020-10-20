import os

import pytest
from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from django.test import RequestFactory, Client
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from ctrack.caf.models import CAF
from ctrack.caf.tests.factories import GradingFactory
from ctrack.core.utils import _create_caf_app_service
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
def user() -> User:
    return UserFactory()


@pytest.fixture
def inspector1() -> User:
    return UserFactory()


@pytest.fixture
def inspector2() -> User:
    return UserFactory()


@pytest.fixture
def submode(inspector1, inspector2):
    return Submode.objects.create(
        descriptor="Light Rail", mode=Mode.objects.create(descriptor="Rail")
    )


@pytest.fixture
def mode():
    return Mode.objects.create(descriptor="Rail")


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
def cct_user(cct_user_group) -> User:
    # For testing views which require redirects to permission-controlled
    # pages, we have to ensure our test user is has the requisite permissions here
    return UserFactory(groups=[cct_user_group])


@pytest.fixture
def person(user, submode, org_with_people):
    org = org_with_people
    role = RoleFactory.create(name="Compliance Inspector")
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
def caf(org) -> CAF:
    # Quality gradings
    q_descriptors = ["Q1", "Q2", "Q3", "Q4", "Q5"]
    for g in q_descriptors:
        GradingFactory.create(descriptor=g, type="QUALITY")

    # Confidence gradings
    c_descriptors = ["C1", "C2", "C3", "C4", "C5"]
    for g in c_descriptors:
        GradingFactory.create(descriptor=g, type="CONFIDENCE")
    caf = _create_caf_app_service(c_descriptors, org, q_descriptors)
    return caf


@pytest.fixture
def browser(request):
    "Provide selenium webdriver instance."
    os.environ["PATH"] += os.pathsep + os.getcwd()
    options = Options()
    options.headless = True
    browser_ = webdriver.Firefox(firefox_options=options)
    yield browser_
    browser_.quit()


@pytest.fixture
def client(user):
    client = Client()
    client.force_login(user)
    return client
