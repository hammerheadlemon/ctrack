import random

import pytest
from slugify import slugify

from ctrack.caf.models import CAF, Grading
from ctrack.caf.models import EssentialService
from ctrack.caf.tests.factories import ApplicableSystemFactory
from ctrack.core.utils import fnames
from ctrack.organisations.tests.factories import PersonFactory, SingleDateTimeEventFactory

pytestmark = pytest.mark.django_db


def test_get_people(org, person):
    person.organisation = org
    person.save()
    assert person in org.get_people()


def test_lead_deputy_inspector(org):
    assert org.lead_inspector
    assert org.deputy_lead_inspector


def test_organisation_get_absolute_url(org):
    slug = slugify(org.name)
    assert org.get_absolute_url() == f"/organisations/{slug}/"


def test_can_get_all_single_datetime_events_involving_person(person):
    e = SingleDateTimeEventFactory.create(type_descriptor="MEETING", short_description="No desc")
    e.participants.add(person)
    events_involving_person = person.get_single_datetime_events()
    assert events_involving_person.first().short_description == "No desc"


def test_update_organisation(org_with_people):
    # Change the name of the organisation
    org_with_people.name = "Tonkers Ltd"
    org_with_people.save()
    assert org_with_people.name == "Tonkers Ltd"


def test_new_address(addr):
    # The address "has" an organisation
    assert addr.organisation.name


def test_essential_service(org):
    q1 = Grading.objects.create(descriptor="Q1", description="baws", type="QUALITY")
    c1 = Grading.objects.create(
        descriptor="C1", description="baws_c", type="CONFIDENCE"
    )
    caf = CAF.objects.create(
        quality_grading=q1,
        organisation=org,
        confidence_grading=c1,
        triage_review_date=None,
        triage_review_inspector=None,
    )
    ass = ApplicableSystemFactory.create(name=random.choice(fnames), caf=caf, )
    ass2 = ApplicableSystemFactory.create(name=random.choice(fnames), caf=caf, )
    es = EssentialService.objects.create(
        name="Test ES", description="Test ES Description", organisation=org
    )
    es.systems.add(ass, ass2)
    assert es.organisation.name == org.name
    assert es.name == "Test ES"
    assert es.systems.count() == 2
    assert ass.name in [s.name for s in org.systems()]
