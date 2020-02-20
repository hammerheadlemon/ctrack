from django.core.management import BaseCommand
from django.core.management import CommandParser

from ctrack.organisations.tests.factories import PersonFactory
from ctrack.organisations.tests.factories import RoleFactory
from ctrack.organisations.tests.factories import UserFactory


class Command(BaseCommand):
    help = """
    Creates a bunch of people and organisations for them to work in.

    Also creates users and roles as these are required fields.
    """

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("number", nargs=1, type=int)

    def handle(self, *args, **options):
        number = options["number"][0]
        user = UserFactory.create()  # we need to have at least one user for the updated_by field
        role = RoleFactory.create()  # because we have a many-to-many relationship with Role, we need to create one and pass it in
        PersonFactory.create_batch(number, role=role, updated_by=user,
                                   predecessor__predecessor=None)  # we do this so we don't get a loop
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {number} Person object[s]! Go forth and multiply."
            )
        )
