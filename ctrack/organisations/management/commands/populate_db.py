import random
from random import randint, choice

from django.core.management import BaseCommand
from django.core.management import CommandParser

from ctrack.assessments.models import CAFSelfAssessment, CAFObjective, CAFPrinciple, CAFContributingOutcome
from ctrack.caf.models import CAF
from ctrack.caf.tests.factories import (
    GradingFactory,
    FileStoreFactory,
    CAFFactory,
    ApplicableSystemFactory,
)
from ctrack.organisations.models import AddressType, Person
from ctrack.organisations.models import Mode
from ctrack.organisations.models import Submode
from ctrack.organisations.tests.factories import AddressFactory
from ctrack.organisations.tests.factories import OrganisationFactory
from ctrack.organisations.tests.factories import PersonFactory
from ctrack.organisations.tests.factories import RoleFactory
from ctrack.organisations.tests.factories import UserFactory
from ctrack.register.tests.factories import EngagementEventFactory
from ctrack.register.tests.factories import EngagementTypeFactory

fnames = [
    "Clock Pylon Systems",
    "Ultramarine Hanglider Navigator",
    "Membranous Floor Heaters",
    "Alan's Wardrobe Hinge Circuits",
    "Marine Sluicegate Extension Pulleys",
    "Ironway Prob Modelling Area",
    "Bufferage Clippers",
    "Slow Gauze Thread Manipulator",
    "Terratoast Piling",
    "Accounting and Warehouse Conducer",
    "Able Hopscotch Mirrors",
    "Jolly Main Legacy Circuitry",
]


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

        inspector_role = RoleFactory.create(name="Compliance Inspector")

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

        regulator_org = OrganisationFactory.create(
            submode=None,
            name="The Regulator",
            designation_type=3,
            registered_company_name="The Regulator - HMG",
            comments="This is the real regulator.",
        )

        inspectors = [
            PersonFactory.create(
                role=inspector_role,
                updated_by=user,
                job_title="Compliance Inspector",
                predecessor=None,
                organisation__submode=None,
                organisation=regulator_org,
            )
            for _ in range(5)
        ]

        etf1 = EngagementTypeFactory(descriptor="Information Notice")
        etf2 = EngagementTypeFactory(descriptor="Designation Letter")
        etf3 = EngagementTypeFactory(
            descriptor="CAF - Initial Submission", enforcement_instrument=False
        )

        EngagementEventFactory.create(type=etf1, user=user, participants=[p1, p2])
        EngagementEventFactory.create(type=etf2, user=user, participants=[p3])

        # Quality gradings
        q_descriptors = ["Q1", "Q2", "Q3", "Q4", "Q5"]
        for g in q_descriptors:
            GradingFactory.create(descriptor=g, type="QUALITY")

        # Confidence gradings
        c_descriptors = ["C1", "C2", "C3", "C4", "C5"]
        for g in c_descriptors:
            GradingFactory.create(descriptor=g, type="CONFIDENCE")

        # File store
        FileStoreFactory.create(physical_location_organisation=orgs[1])

        # Every org gets on CAF for now
        for org in orgs:
            # create a CAF and ApplicableService for it
            self._create_caf_app_service(c_descriptors, org, q_descriptors)

        # CAF submissions - they create EngagementEvents
        # Get a random CAF
        _caf = CAF.objects.get(pk=1)  # we should have one by now
        EngagementEventFactory.create(
            type=etf3, user=user, participants=[inspectors[1], p2], related_caf=_caf
        )

        # We want to create a CAF with a bunch of scoring now...
        _caf2 = CAF.objects.get(pk=1)
        _completer = Person.objects.get(pk=1)
        caf_assessment = CAFSelfAssessment.objects.create(
            caf_id=_caf2.id, completer_id=_completer.id, comments="Random Comments"
        )

        # We want to simulate 4 CAF Objectives
        c_obj_a = CAFObjective.objects.create(name="Objective A: Major Issue A",
                                              description="An important objective to fix the world.", order_id=1)
        c_obj_b = CAFObjective.objects.create(name="Objective B: Major Issue B",
                                              description="An important objective to fix the world.", order_id=2)
        c_obj_c = CAFObjective.objects.create(name="Objective C: Major Issue C",
                                              description="An important objective to fix the world.", order_id=3)
        c_obj_d = CAFObjective.objects.create(name="Objective D: Major Issue D",
                                              description="An important objective to fix the world.", order_id=4)

        # For each Objective, let's create four Principles
        p_a1 = CAFPrinciple.objects.create(
            caf_objective_id=c_obj_a.id,
            designation="A1",
            title="Governance",
            description="When you don't have Governance, you have nothing.",
            order_id=1
        )
        p_a2 = CAFPrinciple.objects.create(
            caf_objective_id=c_obj_a.id,
            designation="A2",
            title="Risk Management",
            description="Don't take a risk, and don't get nowhere.",
            order_id=2
        )
        p_a3 = CAFPrinciple.objects.create(
            caf_objective_id=c_obj_a.id,
            designation="A3",
            title="Asset Management",
            description="Without assets, you have no raw materials to work with.",
            order_id=3
        )
        p_a4 = CAFPrinciple.objects.create(
            caf_objective_id=c_obj_a.id,
            designation="A4",
            title="Supply Chain",
            description="You need to get your stuff from somewhere.",
            order_id=4
        )

        p_b1 = CAFPrinciple.objects.create(
            caf_objective_id=c_obj_b.id,
            designation="B1",
            title="Service Protection & Policies",
            description="Put in place the right protections for a future of security.",
            order_id=1
        )
        p_b2 = CAFPrinciple.objects.create(
            caf_objective_id=c_obj_b.id,
            designation="B2",
            title="Identity and Access Control",
            description="Stop the wrong people getting at your critical assets, okay.",
            order_id=2
        )
        p_b3 = CAFPrinciple.objects.create(
            caf_objective_id=c_obj_b.id,
            designation="B3",
            title="Data Security",
            description="Data is the new oil...",
            order_id=3
        )
        p_b4 = CAFPrinciple.objects.create(
            caf_objective_id=c_obj_b.id,
            designation="B4",
            title="System Security",
            description="If you have complicated systems, they need some sort of security.",
            order_id=4
        )

        # Only two of these
        p_c1 = CAFPrinciple.objects.create(
            caf_objective_id=c_obj_c.id,
            designation="C1",
            title="Security Monitoring",
            description="Monitoring the bits and pieces is the most important aspect of your life.",
            order_id=1
        )
        p_c2 = CAFPrinciple.objects.create(
            caf_objective_id=c_obj_c.id,
            designation="C2",
            title="Proactive Security and Event Discovery",
            description="If we're not proactive, we will get found out eventually.",
            order_id=2
        )

        # Only two of these too
        p_d1 = CAFPrinciple.objects.create(
            caf_objective_id=c_obj_d.id,
            designation="D1",
            title="Response and Recovery Planning",
            description="Responding to the security problems since 1999...",
            order_id=1
        )
        p_d2 = CAFPrinciple.objects.create(
            caf_objective_id=c_obj_d.id,
            designation="D2",
            title="Improvements",
            description="Improving all the things.",
            order_id=2
        )

        # Based on these principles, it's time to gen some CAFContributingOutcomes
        p_a1_co_a = CAFContributingOutcome.objects.create(
            designation="A1.a",
            name="Board Direction",
            description="You have forced your Board to listen to your whinging about cyber.",
            principle_id=p_a1.id,
            order_id=1
        )

        p_a1_co_b = CAFContributingOutcome.objects.create(
            designation="A1.b",
            name="Roles and Responsibilities",
            description="Your elders and betters are impressed and they continue to make money after your project "
                        "implementation.",
            principle_id=p_a1.id,
            order_id=2
        )

        p_a1_co_c = CAFContributingOutcome.objects.create(
            designation="A1.c",
            name="Decision-making",
            description="If you are forced to participate in the Crystal Maze, you'll choose the coorect path across "
                        "the Gordian runway.",
            principle_id=p_a1.id,
            order_id=3
        )

        p_a2_co_a = CAFContributingOutcome.objects.create(
            designation="A2.a",
            name="Risk Management Process",
            description="You take mighty risks, but they are mitigated by more sensible people around you - good.",
            principle_id=p_a2.id,
            order_id=1
        )

        p_a2_co_b = CAFContributingOutcome.objects.create(
            designation="A2.b",
            name="Assurance",
            description="We all make mistakes, but in doing this well you at least have told people what you're doing.",
            principle_id=p_a2.id,
            order_id=2
        )

        p_a3_co_a = CAFContributingOutcome.objects.create(
            designation="A3.a",
            name="Asset Management",
            description="Taking care of these aspects of corporate life is commensurate with the money-making way.",
            principle_id=p_a3.id,
            order_id=1
        )

        p_a4_co_a = CAFContributingOutcome.objects.create(
            designation="A4.a",
            name="Supply Chain",
            description="Task your customers to take on all the risk, the debt, the hassle - you're good to go.",
            principle_id=p_a4.id,
            order_id=1
        )
        # TODO - adapt this so that it records more than just Persons created

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {number} Person object[s]! Go forth and multiply."
            )
        )

    def _create_caf_app_service(self, c_descriptors, org, q_descriptors):
        caf = CAFFactory.create(
            quality_grading__descriptor=random.choice(q_descriptors),
            confidence_grading__descriptor=random.choice(c_descriptors),
            triage_review_date=None,
            triage_review_inspector=None,
        )
        # Each CAF can have up to three systems associated with it
        for _ in range(random.randint(1, 3)):
            ApplicableSystemFactory.create(
                name=random.choice(fnames), organisation=org, caf=caf,
            )
