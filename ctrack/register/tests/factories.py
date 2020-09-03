import factory
import string
import random

from django.utils import timezone

from django.contrib.auth import get_user_model
from factory import post_generation, Faker

from ctrack.register.models import EngagementEvent
from ctrack.register.models import EngagementType

User = get_user_model()


def _regulation_scrambler():
    reg_type = ["Act", "Regulations", "Directive"]
    reg_titles = [
        "NIS",
        "ISO",
        "NIRST",
        "BIRST",
        "Civil Communications",
        "Paralegal Consequences",
        "Marine and Inner-Waters",
        "Rail Bridges and Overhead Wires",
        "Internal Platform Sewage",
        "Electrical Wires",
        "Cyber Consciousness",
    ]
    section = ["Paragraph", "Section", "Appendix", "Chapter"]
    return (
        f"{random.choice(reg_titles)} {random.choice(reg_type)} "
        f"{str(random.randint(1945, 2020))} - "
        f"{random.choice(section)} {str(random.randint(1, 100))}({random.choice(string.ascii_lowercase[:3])})"
    )


class EngagementTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EngagementType

    descriptor = "Generic Engagement Type"
    enforcement_instrument = True
    regulation_reference = factory.LazyFunction(_regulation_scrambler)


class EngagementEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EngagementEvent

    @post_generation
    def participants(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for p in extracted:
                self.participants.add(p)

    type = factory.SubFactory(EngagementTypeFactory)
    short_description = factory.LazyAttribute(lambda o: f"An event related to {o.type.descriptor}")
    # particpants fed in
    # user fed in
    date = factory.LazyFunction(timezone.now)
    end_date = factory.LazyFunction(timezone.now)
    document_link = factory.Faker("uri")
    response_date_requested = factory.LazyFunction(timezone.now)
    response_received = None
    related_caf = None
    comments = Faker("paragraph", nb_sentences=5, variable_nb_sentences=True, ext_word_list=None)
