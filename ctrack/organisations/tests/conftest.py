
# TODO Here we need to make use of the populate script to create a massive
#      test fixture.
import pytest

from ctrack.core.utils import populate_db


@pytest.fixture
def full_db_fixture():
    populate_db(orgs=2, igps=2)
