"""
THIS TEST IS FROM REALPYTHON ARTICLE
https://realpython.com/django-pytest-fixtures/

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


def test_should_create_user(user_A: get_user_model()) -> None:
    assert user_A.username == "A"


def test_user_is_in_app_user_group(user_A: get_user_model()) -> None:
    assert user_A.groups.filter(name="cct_user").exists()
