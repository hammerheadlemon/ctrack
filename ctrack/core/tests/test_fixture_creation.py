"""
We want to profile the fixture creation function so that we can make it more acceptable for use in tests.
"""
import pytest

from ctrack.core.utils import populate_db

pytestmark = pytest.mark.django_db


def test_core_populate_func():
    populate_db(orgs=2, igps=2)
    assert True
