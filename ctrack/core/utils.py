import random
from random import choice, randint

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from faker import Faker

from ctrack.assessments.models import (
    IGP,
    AchievementLevel,
    CAFAssessment,
    CAFAssessmentOutcomeScore,
    CAFContributingOutcome,
    CAFObjective,
    CAFPrinciple,
)
from ctrack.caf.models import CAF, EssentialService
from ctrack.caf.tests.factories import (
    ApplicableSystemFactory,
    CAFFactory,
    FileStoreFactory,
    GradingFactory,
)
from ctrack.organisations.models import AddressType, Mode, Person, Submode
from ctrack.organisations.tests.factories import (
    AddressFactory,
    OrganisationFactory,
    PersonFactory,
    RoleFactory,
)
from ctrack.register.tests.factories import (
    EngagementEventFactory,
    EngagementTypeFactory,
)
from ctrack.users.tests.factories import UserFactory

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


def _create_caf_app_service(c_descriptors, org, q_descriptors):
    # Get the essential services and systems belonging to the org

    es = EssentialService.objects.create(
        name="".join(["Essential Service for ", org.name]),
        description="Random description",
        organisation=org,
    )
    as1 = ApplicableSystemFactory.create(name=random.choice(fnames))
    as2 = ApplicableSystemFactory.create(name=random.choice(fnames))
    es.systems.add(as1, as2)

    caf = CAFFactory.create(
        quality_grading__descriptor=random.choice(q_descriptors),
        confidence_grading__descriptor=random.choice(c_descriptors),
        organisation=org,
        triage_review_date=None,
        triage_review_inspector=None,
    )
    caf.systems.add(as1, as2)
    return caf


def populate_db(**kwargs):
    # We want the fixtures to be created quicker under unit test conditions,
    # so we can pass in these kwargs to reduce entities created - and omit them
    # from management command populate script.
    _org_number = kwargs.get("orgs")
    _igp_number = kwargs.get("igps")

    # Groups
    cct_staff_group = Group.objects.create(name="cct_users")
    ctrack_permissions = Permission.objects.filter(
        Q(codename__contains="address")
        | Q(codename__contains="addresstype")
        | Q(codename__contains="mode")
        | Q(codename__contains="organisation")
        | Q(codename__contains="role")
        | Q(codename__contains="submode")
        | Q(codename__contains="person")
        | Q(codename__contains="applicablesystem")
        | Q(codename__contains="caf")
        | Q(codename__contains="documentfile")
        | Q(codename__contains="filestore")
        | Q(codename__contains="grading")
        | Q(codename__contains="engagementtype")
        | Q(codename__contains="engagementevent")
        | Q(codename__contains="cafassessment")
        | Q(codename__contains="cafobjective")
        | Q(codename__contains="cafprinciple")
        | Q(codename__contains="cafcontributingoutcome")
        | Q(codename__contains="cafassessmentoutcomescore")
        | Q(codename__contains="achievmentlevel")
        | Q(codename__contains="igp")
        | Q(codename__contains="stakeholder")
        | Q(codename__contains="incidentreport")
    )
    cct_staff_group.permissions.add(*ctrack_permissions)

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

    user = UserFactory.create()

    # Create 40 Organisation objects
    if _org_number:
        orgs = [
            OrganisationFactory.create(submode=submodes[randint(0, len(submodes) - 1)])
            for org in range(_org_number)
        ]
    else:
        orgs = [
            OrganisationFactory.create(submode=submodes[randint(0, len(submodes) - 1)])
            for org in range(40)
        ]

    # Create Address objects
    addr_type = AddressType.objects.create(descriptor="Primary Address")
    for org in orgs:
        AddressFactory.create(type=addr_type, organisation=org)

    roles = [
        RoleFactory.create() for _ in range(10)
    ]  # because we have a many-to-many relationship with Role, we need to create one and pass it in
    for org in orgs:
        PersonFactory.create(
            role=choice(roles),
            predecessor=None,
            organisation__submode=choice(submodes),
            organisation=org,
        )

    inspector_role = RoleFactory.create(name="Compliance Inspector")

    # set up some EngagementEvents

    # noinspection PyUnboundLocalVariable
    p1 = PersonFactory.create(
        role=choice(roles),
        predecessor=None,
        organisation__submode=choice(submodes),
        organisation=org,
    )
    p2 = PersonFactory.create(
        role=choice(roles),
        predecessor=None,
        organisation__submode=choice(submodes),
        organisation=org,
    )
    p3 = PersonFactory.create(
        role=choice(roles),
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
            job_title="Compliance Inspector",
            predecessor=None,
            organisation__submode=None,
            organisation=regulator_org,
        )
        for _ in range(5)
    ]
    inspector_user = get_user_model().objects.create(
        username="inspector1", name="inspector1"
    )
    inspector_user.groups.add(cct_staff_group)

    etf1 = EngagementTypeFactory(descriptor="Information Notice", enforcement_instrument=True)
    etf2 = EngagementTypeFactory(descriptor="Designation Letter", enforcement_instrument=True)
    etf3 = EngagementTypeFactory(
        descriptor="CAF - Received from OES (Egress)", enforcement_instrument=False
    )
    EngagementTypeFactory(descriptor="Phone Call", enforcement_instrument=False)
    EngagementTypeFactory(
        descriptor="Video Conference", enforcement_instrument=False
    )
    EngagementTypeFactory.create(descriptor="Email", enforcement_instrument=False)
    EngagementTypeFactory.create(descriptor="CAF - Initial Review", enforcement_instrument=False)
    EngagementTypeFactory.create(descriptor="CAF - Peer Review")
    EngagementTypeFactory.create(descriptor="CAF - Validation")
    EngagementTypeFactory.create(descriptor="CAF - Sent to Rosa")
    EngagementTypeFactory.create(descriptor="CAF - Received from OES (USB)")
    EngagementTypeFactory.create(descriptor="Audit - Onsite")
    EngagementTypeFactory.create(descriptor="Audit - Offsite")
    EngagementTypeFactory.create(descriptor="Inspection - Onsite")
    EngagementTypeFactory.create(descriptor="Inspection - Offsite")

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

    # Every org gets on CAF and Essential Service for now
    for org in orgs:
        # create a CAF
        _create_caf_app_service(c_descriptors, org, q_descriptors)

    # CAF submissions - they create EngagementEvents
    # Get a random CAF
    _caf = CAF.objects.get(pk=1)  # we should have one by now
    EngagementEventFactory.create(
        type=etf2, user=user, participants=[inspectors[1], p2], related_caf=_caf
    )

    # We want to simulate 4 CAF Objectives
    c_obj_a = CAFObjective.objects.create(
        name="Objective A: Managing security risk",
        description="An important objective to fix the world.",
        order_id=1,
    )
    c_obj_b = CAFObjective.objects.create(
        name="Objective B: Protecting Against Cyber Attack",
        description="An important objective to fix the world.",
        order_id=2,
    )
    c_obj_c = CAFObjective.objects.create(
        name="Objective C: Detecting Cyber Security Events",
        description="An important objective to fix the world.",
        order_id=3,
    )
    c_obj_d = CAFObjective.objects.create(
        name="Objective D: Minimising the Impact of Cyber Security Incidents",
        description="An important objective to fix the world.",
        order_id=4,
    )

    # For each Objective, let's create four Principles
    p_a1 = CAFPrinciple.objects.create(
        caf_objective_id=c_obj_a.id,
        designation="A1",
        title="Governance",
        description="When you don't have Governance, you have nothing.",
        order_id=1,
    )
    p_a2 = CAFPrinciple.objects.create(
        caf_objective_id=c_obj_a.id,
        designation="A2",
        title="Risk Management",
        description="Don't take a risk, and don't get nowhere.",
        order_id=2,
    )
    p_a3 = CAFPrinciple.objects.create(
        caf_objective_id=c_obj_a.id,
        designation="A3",
        title="Asset Management",
        description="Without assets, you have no raw materials to work with.",
        order_id=3,
    )
    p_a4 = CAFPrinciple.objects.create(
        caf_objective_id=c_obj_a.id,
        designation="A4",
        title="Supply Chain",
        description="You need to get your stuff from somewhere.",
        order_id=4,
    )

    p_b1 = CAFPrinciple.objects.create(
        caf_objective_id=c_obj_b.id,
        designation="B1",
        title="Service Protection & Policies",
        description="Put in place the right protections for a future of security.",
        order_id=1,
    )
    p_b2 = CAFPrinciple.objects.create(
        caf_objective_id=c_obj_b.id,
        designation="B2",
        title="Identity and Access Control",
        description="Stop the wrong people getting at your critical assets, okay.",
        order_id=2,
    )
    p_b3 = CAFPrinciple.objects.create(
        caf_objective_id=c_obj_b.id,
        designation="B3",
        title="Data Security",
        description="Data is the new oil...",
        order_id=3,
    )
    p_b4 = CAFPrinciple.objects.create(
        caf_objective_id=c_obj_b.id,
        designation="B4",
        title="System Security",
        description="If you have complicated systems, they need some sort of security.",
        order_id=4,
    )

    p_b5 = CAFPrinciple.objects.create(
        caf_objective_id=c_obj_b.id,
        designation="B5",
        title="Resilience Networks and Systems",
        description="When all else fails, there is always food to be cooked.",
        order_id=5,
    )

    p_b6 = CAFPrinciple.objects.create(
        caf_objective_id=c_obj_b.id,
        designation="B6",
        title="Staff Awareness and Training",
        description="You must ensure your people are trained and equipped for making a difference.",
        order_id=6,
    )

    # Only two of these
    p_c1 = CAFPrinciple.objects.create(
        caf_objective_id=c_obj_c.id,
        designation="C1",
        title="Security Monitoring",
        description="Monitoring the bits and pieces is the most important aspect of your life.",
        order_id=1,
    )
    p_c2 = CAFPrinciple.objects.create(
        caf_objective_id=c_obj_c.id,
        designation="C2",
        title="Proactive Security and Event Discovery",
        description="If we're not proactive, we will get found out eventually.",
        order_id=2,
    )

    # Only two of these too
    p_d1 = CAFPrinciple.objects.create(
        caf_objective_id=c_obj_d.id,
        designation="D1",
        title="Response and Recovery Planning",
        description="Responding to the security problems since 1999...",
        order_id=1,
    )
    p_d2 = CAFPrinciple.objects.create(
        caf_objective_id=c_obj_d.id,
        designation="D2",
        title="Improvements",
        description="Improving all the things.",
        order_id=2,
    )

    # Based on these principles, it's time to gen some CAFContributingOutcomes
    cos = [
        CAFContributingOutcome.objects.create(
            designation="A1.a",
            name="Board Direction",
            description="You have forced your Board to listen to your whinging about cyber.",
            principle_id=p_a1.id,
            order_id=1,
        ),
        CAFContributingOutcome.objects.create(
            designation="A1.b",
            name="Roles and Responsibilities",
            description="Your elders and betters are impressed and they continue to make money after your project "
                        "implementation.",
            principle_id=p_a1.id,
            order_id=2,
        ),
        CAFContributingOutcome.objects.create(
            designation="A1.c",
            name="Decision-making",
            description="If you are forced to participate in the Crystal Maze, you'll choose the coorect path across "
                        "the Gordian runway.",
            principle_id=p_a1.id,
            order_id=3,
        ),
        CAFContributingOutcome.objects.create(
            designation="A2.a",
            name="Risk Management Process",
            description="You take mighty risks, but they are mitigated by more sensible people around you - good.",
            principle_id=p_a2.id,
            order_id=1,
        ),
        CAFContributingOutcome.objects.create(
            designation="A2.b",
            name="Assurance",
            description="We all make mistakes, but in doing this well you at least have told people what you're doing.",
            principle_id=p_a2.id,
            order_id=2,
        ),
        CAFContributingOutcome.objects.create(
            designation="A3.a",
            name="Asset Management",
            description="Taking care of these aspects of corporate life is commensurate with the money-making way.",
            principle_id=p_a3.id,
            order_id=1,
        ),
        CAFContributingOutcome.objects.create(
            designation="A4.a",
            name="Supply Chain",
            description="Task your customers to take on all the risk, the debt, the hassle - you're good to go.",
            principle_id=p_a4.id,
            order_id=1,
        ),
        CAFContributingOutcome.objects.create(
            designation="B1.a",
            name="Policy and Process Development",
            description="You are getting your process and policy development spot on.",
            principle_id=p_b1.id,
            order_id=1,
        ),
        CAFContributingOutcome.objects.create(
            designation="B1.b",
            name="Policy and Process Information",
            description="Differs from the above in a few ways that will be discussed at a later date.",
            principle_id=p_b1.id,
            order_id=2,
        ),
        CAFContributingOutcome.objects.create(
            designation="B2.a",
            name="ID Verification, Authentication and Authorisation",
            description="It is very important for people to be able to confirm they they truly are. Underneath.",
            principle_id=p_b2.id,
            order_id=1,
        ),
        CAFContributingOutcome.objects.create(
            designation="B2.b",
            name="Device Management",
            description="Your devices, and their safe and sustainable use, is crucuial to the longevity of your "
                        "company.",
            principle_id=p_b2.id,
            order_id=2,
        ),
        CAFContributingOutcome.objects.create(
            designation="B2.c",
            name="Privileged User Mangement",
            description="You ensure that even the most privileged members of your senior management are under the "
                        "impression that they exude inequality, in all instances.",
            principle_id=p_b2.id,
            order_id=3,
        ),
        CAFContributingOutcome.objects.create(
            designation="B3.a",
            name="Understanding Data",
            description="You, more than anyone else in the organisation, know what your data means to you.",
            principle_id=p_b3.id,
            order_id=1,
        ),
        CAFContributingOutcome.objects.create(
            designation="B3.b",
            name="Data in Transit",
            description="You are protecting your data as it moves along the Information Superhighway.",
            principle_id=p_b3.id,
            order_id=2,
        ),
        CAFContributingOutcome.objects.create(
            designation="B3.c",
            name="Stored Data",
            description="You have stored your data in accordance with local environment laws.",
            principle_id=p_b3.id,
            order_id=3,
        ),
        CAFContributingOutcome.objects.create(
            designation="B3.d",
            name="Mobile Data",
            description="Mobile data is when data moves because it is stored in a moving thing.",
            principle_id=p_b3.id,
            order_id=4,
        ),
        CAFContributingOutcome.objects.create(
            designation="B3.e",
            name="Media/Equipment Sanitisation",
            description="You routinely wash and clean the legs and bottom brackets of your server racks.",
            principle_id=p_b3.id,
            order_id=5,
        ),
        CAFContributingOutcome.objects.create(
            designation="B4.a",
            name="Secure by Design",
            description="You have designed your systems to be secure and you're sure no one is going to hack "
                        "into them.",
            principle_id=p_b4.id,
            order_id=1,
        ),
        CAFContributingOutcome.objects.create(
            designation="B4.b",
            name="Secure Configuration",
            description="When you are able to configure your systems and software well, you can say you have Secure "
                        "Configuration. Only then, mind.",
            principle_id=p_b4.id,
            order_id=2,
        ),
        CAFContributingOutcome.objects.create(
            designation="B4.c",
            name="Secure Management",
            description="Somehow this one is different from all the others but I'm not sure how.",
            principle_id=p_b4.id,
            order_id=3,
        ),
        CAFContributingOutcome.objects.create(
            designation="B4.d",
            name="Vulnerability Management",
            description="Doing this well means that you are at the top of your vulnerability scale.",
            principle_id=p_b4.id,
            order_id=4,
        ),
        CAFContributingOutcome.objects.create(
            designation="B5.a",
            name="Resilience Preparation",
            description="Totally ready for the coming of the cyber apocalyse. You practice this stuff regular.",
            principle_id=p_b5.id,
            order_id=1,
        ),
        CAFContributingOutcome.objects.create(
            designation="B5.b",
            name="Design for Resilience",
            description="This stuff is built into your very working model.",
            principle_id=p_b5.id,
            order_id=2,
        ),
        CAFContributingOutcome.objects.create(
            designation="B5.c",
            name="Backups",
            description="There is nowhere for you to go as a professional if you don't make backups of your data.",
            principle_id=p_b5.id,
            order_id=3,
        ),
        CAFContributingOutcome.objects.create(
            designation="B6.a",
            name="Cyber Security Culture",
            description="You're making them understand that this isn't going to go away in a hurry.",
            principle_id=p_b6.id,
            order_id=1,
        ),
        CAFContributingOutcome.objects.create(
            designation="B6.b",
            name="Cyber Security Training",
            description="By the way, when youre staff are able to write C code, your company understands buffer "
                        "overflows.",
            principle_id=p_b6.id,
            order_id=2,
        ),
        CAFContributingOutcome.objects.create(
            designation="C1.a",
            name="Monitoring Coverage",
            description="At all times, you are vigilent to the threats out there, and ready to tackle them.",
            principle_id=p_c1.id,
            order_id=1,
        ),
        CAFContributingOutcome.objects.create(
            designation="C1.b",
            name="Securing Logs",
            description="You might think the are a waste of time, but the Board thinks logging is important.",
            principle_id=p_c1.id,
            order_id=2,
        ),
        CAFContributingOutcome.objects.create(
            designation="C1.c",
            name="Generating Alerts",
            description="Boo! There, you coped with it because you're good at this.",
            principle_id=p_c1.id,
            order_id=3,
        ),
        CAFContributingOutcome.objects.create(
            designation="C1.d",
            name="Identifying Security Incidents",
            description="You are wary of all the possible things that could go wrong and you have a plan to deal. Well "
                        "done.",
            principle_id=p_c1.id,
            order_id=4,
        ),
        CAFContributingOutcome.objects.create(
            designation="C1.e",
            name="Monitoring Tools and Skills",
            description="All these things matter in today's switched on cyber-aware environment.",
            principle_id=p_c1.id,
            order_id=5,
        ),
        CAFContributingOutcome.objects.create(
            designation="C2.a",
            name="System Abnormalities for Attack Detection",
            description="Make sure you know how to look for things that mighty wrong on your network.",
            principle_id=p_c2.id,
            order_id=1,
        ),
        CAFContributingOutcome.objects.create(
            designation="C2.b",
            name="Proactive Attack Discovery",
            description="When you go out looking for the bad stuff, you usefully find it - "
                        "and you know this in spades.",
            principle_id=p_c2.id,
            order_id=2,
        ),
        CAFContributingOutcome.objects.create(
            designation="D1.a",
            name="Response Plan",
            description="Yeah, we know it's boring but you've got to have one.",
            principle_id=p_d1.id,
            order_id=1,
        ),
        CAFContributingOutcome.objects.create(
            designation="D1.b",
            name="Response and Recovery Capability",
            description="If you can't get back on your feet after you've been beat, where are you, really?",
            principle_id=p_d1.id,
            order_id=2,
        ),
        CAFContributingOutcome.objects.create(
            designation="D1.c",
            name="Testing and Exercising",
            description="One of the most important things you should not be forgetting is this.",
            principle_id=p_d1.id,
            order_id=3,
        ),
        CAFContributingOutcome.objects.create(
            designation="D2.a",
            name="Incident Root Cause and Analysis",
            description="I guess there are always lessons learned, no matter how we good we are.",
            principle_id=p_d2.id,
            order_id=1,
        ),
        CAFContributingOutcome.objects.create(
            designation="D2.b",
            name="Using Incidents to Drive Improvements",
            description="This is the kind of thing that bores us to tears but it simply has to be done.",
            principle_id=p_d2.id,
            order_id=2,
        ),
    ]

    achievement_levels = [
        AchievementLevel.objects.create(
            descriptor="Not Achieved", colour_description="Red", colour_hex="#000001"
        ),
        AchievementLevel.objects.create(
            descriptor="Partially Achieved",
            colour_description="Amber",
            colour_hex="#000002",
        ),
        AchievementLevel.objects.create(
            descriptor="Achieved", colour_description="Green", colour_hex="#000003"
        ),
    ]

    for al in achievement_levels:
        if _igp_number:
            for co in cos:
                for igp in range(1, _igp_number):
                    dtext_fake = Faker()
                    fake_txt = f"IGP {igp}/{al.descriptor}/{co.designation}: {dtext_fake.paragraph()}"
                    IGP.objects.create(
                        achievement_level=al,
                        contributing_outcome=co,
                        descriptive_text=fake_txt,
                    )
        else:
            for co in cos:
                for igp in range(1, random.randint(2, 5)):
                    dtext_fake = Faker()
                    fake_txt = f"IGP {igp}/{al.descriptor}/{co.designation}: {dtext_fake.paragraph()}"
                    IGP.objects.create(
                        achievement_level=al,
                        contributing_outcome=co,
                        descriptive_text=fake_txt,
                    )

    # We want to create a CAF with a bunch of scoring now...
    _caf2 = CAF.objects.get(pk=1)

    _completer = Person.objects.get(pk=1)
    caf_assessment = CAFAssessment.objects.create(
        caf_id=_caf2.id, completer_id=_completer.id, comments="Random Comments"
    )

    # TODO Need to create as many of these as there are ContributingOutcomes
    # Create a single CAFSelfAssessmentOutcomeScore
    for c in cos:
        CAFAssessmentOutcomeScore.objects.create(
            caf_assessment_id=caf_assessment.id,
            caf_contributing_outcome_id=c.id,
            assessment_score=random.choice(
                ["Achieved", "Partially Achieved", "Not Achieved"]
            ),
            baseline_assessment_score=random.choice(
                ["Achieved", "Partially Achieved", "Not Achieved"]
            ),
        )
