from typing import Any, Sequence

from django.contrib.auth import get_user_model
from ctrack.organisations.models import Organisation, Address
from factory import DjangoModelFactory, Faker, post_generation


class OrganisationFactory(DjangoModelFactory):

    name = Faker("company", locale="en_GB")

    class Meta:
        model = Organisation


class AddressFactory(DjangoModelFactory):
    line1 = Faker("secondary_address", locale="en_GB")
    line2 = Faker("street_name", locale="en_GB")
    line3 = Faker("secondary_address", locale="en_GB")
    city = Faker("city", locale="en_GB")
    county = Faker("lexify", locale="en_GB", text="??????", letters="aeioutzyj")
    postcode = Faker("postcode", locale="en_GB")
    country = Faker("country")
    other_details = Faker("lexify", locale="en_GB", text="??????", letters="aeioutzyj")

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
