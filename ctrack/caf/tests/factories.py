import factory

from factory import Faker

from ctrack.caf.models import CAF, EssentialService, Grading
from ctrack.organisations.tests.factories import PersonFactory


class EssentialServiceFactory(factory.DjangoModelFactory):
    """Factory for Essential Services."""

    class Meta:
        model = EssentialService


class GradingFactory(factory.DjangoModelFactory):
    descriptor = factory.Iterator(["Q1", "Q2", "Q3", "Q4", "Q5", "C1", "C2", "C3", "C4", "C5"])
    description = Faker("text", max_nb_chars=100, ext_word_list=None)
    type = factory.Iterator(Grading.GRADING_TYPE, getter=lambda g: g[0])

    class Meta:
        model = Grading


class CAFFactory(factory.DjangoModelFactory):
    """Factory for CAFs."""
    owner = factory.SubFactory(PersonFactory)
#   triage_ranking = factory.SubFactory(TriageRankingFactory)

    class Meta:
        model = CAF
