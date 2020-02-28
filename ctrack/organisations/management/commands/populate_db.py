import random
from random import randint, choice

from django.core.management import BaseCommand
from django.core.management import CommandParser

from ctrack.caf.tests.factories import GradingFactory, FileStoreFactory, CAFFactory
from ctrack.organisations.models import AddressType
from ctrack.organisations.models import Mode
from ctrack.organisations.models import Submode
from ctrack.organisations.tests.factories import AddressFactory
from ctrack.organisations.tests.factories import OrganisationFactory
from ctrack.organisations.tests.factories import PersonFactory
from ctrack.organisations.tests.factories import RoleFactory
from ctrack.organisations.tests.factories import UserFactory
from ctrack.register.tests.factories import EngagementEventFactory
from ctrack.register.tests.factories import EngagementTypeFactory


class Command(BaseCommand):
    help = """
    Creates a bunch of people and organisations for them to work in.

    Also creates users and roles as these are required fields.
    """

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("number", nargs=1, type=int)

    def handle(self, *args, **options):
        number = options["number"][0]

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

        submodes = [sb1, sb2, sb3, sb4, sb5, sb6, sb7]

        # we need a User object to completed the updated_by fields in Organisation and Person
        user = (
            UserFactory.create()
        )  # we need to have at least one user for the updated_by field

        # Create 40 Organisation objects
        orgs = [
            OrganisationFactory.create(submode=submodes[randint(0, len(submodes) - 1)])
            for org in range(40)
        ]
        # Create 40 Address objects
        addr_type = AddressType.objects.create(descriptor="Primary Address")
        for org in orgs:
            AddressFactory.create(type=addr_type, organisation=org)

        roles = [
            RoleFactory.create() for x in range(10)
        ]  # because we have a many-to-many relationship with Role, we need to create one and pass it in
        for org in orgs:
            PersonFactory.create(
                role=choice(roles),
                updated_by=user,
                predecessor=None,
                organisation__submode=choice(submodes),
                organisation=org,
            )
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {number} Person object[s]! Go forth and multiply."
            )
        )

        # set up some EngagementEvents

        p1 = PersonFactory.create(
            role=choice(roles),
            updated_by=user,
            predecessor=None,
            organisation__submode=choice(submodes),
            organisation=org,
        )
        p2 = PersonFactory.create(
            role=choice(roles),
            updated_by=user,
            predecessor=None,
            organisation__submode=choice(submodes),
            organisation=org,
        )
        p3 = PersonFactory.create(
            role=choice(roles),
            updated_by=user,
            predecessor=None,
            organisation__submode=choice(submodes),
            organisation=org,
        )

        etf1 = EngagementTypeFactory(descriptor="Information Notice")
        etf2 = EngagementTypeFactory(descriptor="Designation Letter")

        ee1 = EngagementEventFactory.create(type=etf1, user=user, participants=[p1, p2])
        ee2 = EngagementEventFactory.create(type=etf2, user=user, participants=[p3])

        # Quality gradings
        q_descriptors = ["Q1", "Q2", "Q3", "Q4", "Q5"]
        for g in q_descriptors:
            GradingFactory.create(descriptor=g, type="QUALITY")

        # Confidence gradings
        c_descriptors = ["C1", "C2", "C3", "C4", "C5"]
        for g in c_descriptors:
            GradingFactory.create(descriptor=g, type="CONFIDENCE")

        # File store
        fs = FileStoreFactory.create(physical_location_organisation=orgs[1])

        # Some CAF objects
        for c in range(35):
            CAFFactory.create(
                owner=random.choice(orgs),
                quality_grading__descriptor=random.choice(q_descriptors),
                confidence_grading__descriptor=random.choice(c_descriptors),
            )
