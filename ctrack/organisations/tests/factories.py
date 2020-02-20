import random
from datetime import datetime

import factory
from django.contrib.auth import get_user_model
from factory import DjangoModelFactory, Faker, SubFactory, post_generation

from ctrack.organisations.models import Mode, Organisation, Person, Role, Submode, Address, AddressType

User = get_user_model()


def _random_mode():
    sms = [
        "Aviation",
        "Rail",
        "Maritime",
        "Animal",
        "Stellar",
    ]
    return sms[random.randint(0, len(sms) - 1)]


def _random_submode():
    sms = [
        "Light Rail",
        "Heavy Rail",
        "Passenger Rail",
        "Animal Transport",
        "Infrastructure",
    ]
    return sms[random.randint(0, len(sms) - 1)]


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    name = Faker("name", locale="en_GB")


class ModeFactory(DjangoModelFactory):
    class Meta:
        model = Mode

    descriptor = factory.LazyFunction(_random_mode)


class SubModeFactory(DjangoModelFactory):
    class Meta:
        model = Submode

    descriptor = factory.LazyFunction(_random_submode)
    mode = SubFactory(ModeFactory)


class OrganisationFactory(DjangoModelFactory):
    class Meta:
        model = Organisation

    name = Faker("company")
    slug = Faker("lexify", text="????", letters="abcdsg")
    submode = SubFactory(SubModeFactory)
    designation_type = 1
    registered_company_name = Faker("company")
    registered_company_number = Faker("numerify", text="######")
    date_updated = Faker("date_this_year", before_today=True)
    updated_by = SubFactory(UserFactory)
    comments = Faker("paragraph", nb_sentences=3)
    active = True


class RoleFactory(DjangoModelFactory):
    class Meta:
        model = Role

    name = Faker("job")


class PersonFactory(DjangoModelFactory):
    class Meta:
        model = Person

    @post_generation
    def role(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for role in extracted:
                self.role.add(role)

    primary_nis_contact = True
    voluntary_point_of_contact = True
    has_egress = False
    title = Faker("prefix")
    job_title = Faker("job")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    organisation = SubFactory(OrganisationFactory)
    email = Faker("ascii_company_email")
    secondary_email = "ascii_company_email"
    mobile = Faker("msisdn", locale="en_GB")
    landline = Faker("phone_number", locale="en_GB")
    date_updated = factory.LazyFunction(datetime.now)
    updated_by = SubFactory(UserFactory)
    clearance = factory.LazyFunction(datetime.now)
    clearance_sponsor = Faker("name", locale="en_GB")
    clearance_start_date = factory.LazyFunction(datetime.now)
    clearance_last_checked = factory.LazyFunction(datetime.now)
    clearance_expiry = factory.LazyFunction(datetime.now)
    active = True
    date_ended = Faker("date_this_year")
    predecessor = SubFactory("ctrack.organisations.tests.factories.PersonFactory")
    comments = "Yaa!"


class AddressFactory(DjangoModelFactory):
    type = SubFactory("ctrack.organisations.tests.factories.AddressTypeFactory")
    organisation = SubFactory(OrganisationFactory)
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


class AddressTypeFactory(DjangoModelFactory):
    descriptor = "Primary Address"

    class Meta:
        model = AddressType
