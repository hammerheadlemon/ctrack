from typing import Any, Sequence

from django.contrib.auth import get_user_model
from ctrack.organisations.models import Organisation, Address
from factory import DjangoModelFactory, Faker, post_generation


class OrganisationFactory(DjangoModelFactory):

    name = Faker("name")

    class Meta:
        model = Organisation


class AddressFactory(DjangoModelFactory):
    line1 = Faker("line1")
    line2 = Faker("line2")
    line3 = Faker("line3")
    city = Faker("city")
    county = Faker("county")
    postcode = Faker("postcode")
    country = Faker("country")
    other_details = Faker("other_details")

    class Meta:
        model = Address


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

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]
