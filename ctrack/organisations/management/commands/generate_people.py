from datetime import datetime

import random

import factory
from django.core.management.base import BaseCommand, CommandError
from factory import DjangoModelFactory, Faker, SubFactory, post_generation

from ctrack.organisations.models import Organisation, Person, Submode, Mode


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
    updated_by = SubFactory(
        "ctrack.organisations.management.commands.generate_people.PersonFactory"
    )
    comments = Faker("paragraph", nb_sentences=3)
    active = True


class PersonFactory(DjangoModelFactory):
    class Meta:
        model = Person

    primary_nis_contact = True
    voluntary_point_of_contact = True
    has_egress = False
    title = Faker("prefix")
    job_title = Faker("job")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    organisation = SubFactory(OrganisationFactory)
    role = Faker("job")
    email = Faker("ascii_company_email")
    secondary_email = "ascii_company_email"
    mobile = Faker("msisdn", locale="en_GB")
    landline = Faker("phone_number", locale="en_GB")
    date_updated = factory.LazyFunction(datetime.now)
    updated_by = SubFactory(
        "ctrack.organisations.management.commands.generate_people.PersonFactory"
    )
    clearance = factory.LazyFunction(datetime.now)
    clearance_sponsor = Faker("name", locale="en_GB")
    clearance_start_date = factory.LazyFunction(datetime.now)
    clearance_last_checked = factory.LazyFunction(datetime.now)
    clearance_expiry = factory.LazyFunction(datetime.now)
    active = True
    date_ended = Faker("date_this_year")
    predecessor = SubFactory(
        "ctrack.organisations.management.commands.generate_people.PersonFactory"
    )
    comments = "Yaa!"


class Command(BaseCommand):
    help = """
    Creates a bunch of people and organisations for them to work in.

    python manage.py generate_people
    """


#    def add_arguments(self, parser):
#        parser.add_argument("year", nargs="+", type=int)
#
#    def handle(self, *args, **options):
#        for opt in options["year"]:
#            FinancialQuarter.objects.create(quarter=1, year=opt)
#            FinancialQuarter.objects.create(quarter=2, year=opt)
#            FinancialQuarter.objects.create(quarter=3, year=opt)
#            FinancialQuarter.objects.create(quarter=4, year=opt)
#            self.stdout.write(
#                self.style.SUCCESS(
#                    f"Created FinancialQuarter objects for the years: {opt}"
#                )
#            )
