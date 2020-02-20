from django.core.management import BaseCommand
from django.core.management import CommandParser

from ctrack.organisations.models import Mode
from ctrack.organisations.models import Submode
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

        # Set up some reasonable Modes and SubModes
        m1 = Mode.objects.create(descriptor="Rail")
        m2 = Mode.objects.create(descriptor="Maritime")
        sb1 = Submode.objects.create(descriptor="Light Rail", mode=m1)
        sb2 = Submode.objects.create(descriptor="Rail Maintenance", mode=m1)
        sb3 = Submode.objects.create(descriptor="Rail Infrastructure", mode=m1)
        sb4 = Submode.objects.create(descriptor="International Rail", mode=m1)
        sb5 = Submode.objects.create(descriptor="Passenger Port", mode=m2)
        sb6 = Submode.objects.create(descriptor="Freight Port", mode=m2)
        sb7 = Submode.objects.create(descriptor="Shipping Infrastructure", mode=m2)

        # TODO: Create 40 odd organisations here, get their ids and pass them into PersonFactory.create_batch()
        #       below.  Then we need to write a post_generation hook in PersonFactory which ensures that the person
        #       is only added to these Organisations and no further Organisation objects are created.

        number = options["number"][0]
        user = UserFactory.create()  # we need to have at least one user for the updated_by field
        role = RoleFactory.create()  # because we have a many-to-many relationship with Role, we need to create one and pass it in
        PersonFactory.create_batch(number, role=role, updated_by=user,
                                   predecessor__predecessor=None, organisation__submode=sb1)  # we do this so we don't get a loop
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {number} Person object[s]! Go forth and multiply."
            )
        )
