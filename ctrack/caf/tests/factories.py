import random

import factory
from factory import Faker

from ctrack.caf.models import EssentialService, Grading, DocumentFile, FileStore, CAFFileStore
from ctrack.organisations.tests.factories import OrganisationFactory


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


# TODO: test these two factories
class CAFFileStoreFactory(factory.DjangoModelFactory):
    descriptor = "File Store X"
    virtual_location = Faker("street_name")
    physical_location = random.choice(["Cupboard A", "Tin Box", "The Vault"])
    physical_location_organisation = factory.SubFactory(OrganisationFactory)

    class Meta:
        model = CAFFileStore


class DocumentFileFactory(factory.DjangoModelFactory):
    name = Faker("file_name", extension="xlsx")
    type = random.choice([1, 2, 3, 4])
    file_store_location = factory.SubFactory(CAFFileStoreFactory)

    class Meta:
        model = DocumentFile
