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

    username = Faker("lexify", text="???????", letters="abcdsgTGQA")
    password = Faker("lexify", text="????????", letters="AdOIqkcvBnMP")


class OrganisationFactory(DjangoModelFactory):
    class Meta:
        model = Organisation

    name = Faker("company")
    slug = Faker("lexify", text="????", letters="abcdsg")
#   submode = SubFactory(SubModeFactory)
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

    # @post_generation
    # def organisation(self, create, extracted, **kwargs):
    #     if not create:
    #         return
    #     if extracted:
    #         for org in extracted:
    #             self.organisation.add(org)

    @post_generation
    def role(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.role.add(extracted)

    primary_nis_contact = True
    voluntary_point_of_contact = True
    has_egress = False
    title = factory.LazyFunction(lambda: random.randint(1, 8))
    job_title = Faker("job")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    organisation = SubFactory("ctrack.organisations.tests.factories.OrganisationFactory")
    email = factory.LazyAttribute(lambda o: '%s@%s.com' % (o.first_name.lower(), o.organisation.slug))
    secondary_email = Faker("ascii_company_email")
    mobile = Faker("msisdn", locale="en_GB")
    landline = Faker("phone_number", locale="en_GB")
    date_updated = factory.LazyFunction(datetime.now)
    updated_by = SubFactory(UserFactory)
    clearance = factory.LazyFunction(lambda: random.randint(1,6))
    clearance_sponsor = Faker("name", locale="en_GB")
    clearance_start_date = factory.LazyFunction(datetime.now)
    clearance_last_checked = factory.LazyFunction(datetime.now)
    clearance_expiry = factory.LazyFunction(datetime.now)
    active = True
    date_ended = Faker("date_this_year")
    predecessor = SubFactory("ctrack.organisations.tests.factories.PersonFactory")
    comments = Faker("text", max_nb_chars=500, ext_word_list=None)


class AddressFactory(DjangoModelFactory):
    type = SubFactory("ctrack.organisations.tests.factories.AddressTypeFactory")
    organisation = SubFactory(OrganisationFactory)
    line1 = Faker("building_number", locale="en_GB")
    line2 = Faker("street_name", locale="en_GB")
    line3 = Faker("secondary_address", locale="en_GB")
    city = Faker("city", locale="en_GB")
    county = Faker("lexify", locale="en_GB", text="??????", letters="aeioutzyj")
    postcode = Faker("postcode", locale="en_GB")
    country = "UK"
    other_details = Faker("text", max_nb_chars=200, ext_word_list=None)

    class Meta:
        model = Address

