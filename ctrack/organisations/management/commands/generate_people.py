import factory

from django.core.management.base import BaseCommand, CommandError

from factory import DjangoModelFactory, Faker, post_generation, SubFactory

from ctrack.organisation.models import Person, Organisation


class OrganisationFactory(DjangoModelFactory):
    pass


class PersonFactory(DjangoModelFactory):

    class Meta:
        model = Person

    primary_nis_contact = True
    voluntary_point_of_contact = True
    has_egress = False
    title =  Faker("prefix")
    job_title = Faker("job")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    organisation = SubFactory(OrganisationFactory)
    role =
    email =
    secondary_email =
    mobile = 
    landline =
    date_updated =
    updated_by = 
    clearance =
    clearance_sponsor =
    clearance_start_date = 
    clearance_last_checked = 
    clearance_expiry = 
    active = 
    date_ended = 
    predecessor =
    comments =


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
