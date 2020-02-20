from django.core.management import BaseCommand
from django.core.management import CommandParser

from ctrack.organisations.tests.factories import PersonFactory
from ctrack.organisations.tests.factories import RoleFactory
from ctrack.organisations.tests.factories import UserFactory


class Command(BaseCommand):
    help = """
    Creates a bunch of people and organisations for them to work in.

    python manage.py generate_people
    """

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("number", nargs=1, type=int)

    def handle(self, *args, **options):
        number = options["number"][0]
        # Let's use the factory to create people (and organisations, a user and role as a by-product)
        user = UserFactory.create()
        role = RoleFactory.create()  # all these people get the role for now
        PersonFactory.create_batch(number, role=role, updated_by=user, predecessor=None)  # predecessor is too hard at the moment
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {number} Person object[s]! Go forth and multiply."
            )
        )

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
