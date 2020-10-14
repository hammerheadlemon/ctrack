from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import Faker, post_generation
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = Faker(
            "password",
            length=42,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        ).generate(extra_kwargs={})
        self.set_password(password)

    @post_generation
    def groups(self, create, extracted, **kwargs):
        """We need to allow this user to have groups added to it for permissions."""
        if not create:
            return
        if extracted:
            for group in extracted:
                self.groups.add(group)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]
