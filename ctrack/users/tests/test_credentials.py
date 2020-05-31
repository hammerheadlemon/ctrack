"""
THE INITIATIVE FOR THIS TEST IS FROM REALPYTHON ARTICLE
https://realpython.com/Django-pytest-fixtures/

The permissions here are not optimal for this project yet.
TODO - make them so!
"""
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission


@pytest.fixture
def user_A(db) -> Group:
    group = Group.objects.create(name="cct_user")
    change_user_permissions = Permission.objects.filter(
        codename__in=["change_user", "view_user"],
    )
    group.permissions.add(*change_user_permissions)
    user = get_user_model().objects.create_user("A")
    user.groups.add(group)
    return user


def test_there_is_a_cct_user_group(db):  # adding fixture here
    group = Group.objects.create(name="cct_user")
    assert Group.objects.get(name="cct_user")
    user = get_user_model().objects.create_user(
        username="INSPECTOR", name="Mrs Inspector"
    )
    user.groups.add(group)
    assert group in user.groups.all()


def test_user_fixture_has_access_to_all_ctrack_models(db, cct_user_group):
    view_org_perm = Permission.objects.get(codename="view_organisation")
    assert view_org_perm in cct_user_group.permissions.all()


# def test_should_create_user(user_A: get_user_model()) -> None:
#     assert user_A.username == "A"


# def test_user_is_in_app_user_group(user_A: get_user_model()) -> None:
#     assert user_A.groups.filter(name="cct_user").exists()
