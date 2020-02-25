import factory

from ctrack.caf.models import CAF, EssentialService
from ctrack.organisations.tests.factories import PersonFactory


class EssentialServiceFactory(factory.DjangoModelFactory):
    """Factory for Essential Services."""
    model = EssentialService


class CAFFactory(factory.DjangoModelFactory):
    """Factory for CAFs."""
    model = CAF
    owner = factory.SubFactory(PersonFactory)
#   triage_ranking = factory.SubFactory(TriageRankingFactory)
# TODO - we want an abstract Ranking
