import pytest

pytestmark = pytest.mark.django_db


def test_can_get_cafs_from_applicable_system(caf):
    version = caf.version
    test_system = caf.systems.all().first()
    cafs = test_system.get_cafs()
    assert version in [c.version for c in cafs]
