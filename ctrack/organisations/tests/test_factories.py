from ctrack.organisations.tests.factories import OrganisationFactory
from ctrack.organisations.tests.factories import PersonFactory
from ctrack.organisations.tests.factories import RoleFactory
from ctrack.organisations.tests.factories import UserFactory


def test_user_factory():
    u = UserFactory.build()
    assert u.username


def test_organisation_factory():
    o = OrganisationFactory.build()
    assert o.name


def test_role_factory():
    r = RoleFactory.build()
    assert r.name


def test_person_factory():
    r = RoleFactory.build()
    p = PersonFactory.build(role=r, predecessor__predecessor=None)
    assert p.first_name
