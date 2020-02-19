import pytest

from .factories import (
    PersonFactory,
    ModeFactory,
    SubModeFactory,
    UserFactory,
    OrganisationFactory,
    RoleFactory)


def test_mode_factory():
    m = ModeFactory.build()
    assert m.descriptor


def test_submode_factory():
    sm = SubModeFactory.build()
    assert sm.descriptor
    assert sm.mode


def test_user_factory():
    u = UserFactory.build()
    assert u.name


def test_organisation_factory():
    o = OrganisationFactory.build()
    assert o.name


def test_role_factory():
    r = RoleFactory.build()
    assert r.name


def test_person_factory():
    r = RoleFactory.build()
    p = PersonFactory.build(role=r)
    assert p.first_name
