import random

import factory
from factory import Faker

from ctrack.caf.models import EssentialService, Grading, DocumentFile, FileStore, CAF
from ctrack.organisations.tests.factories import OrganisationFactory


class CAFFactory(factory.DjangoModelFactory):
    owner = factory.SubFactory(OrganisationFactory)
    quality_grading = factory.SubFactory("ctrack.caf.tests.factories.GradingFactory")
    confidence_grading = factory.SubFactory("ctrack.caf.tests.factories.GradingFactory")
    file = None

    class Meta:
        model = CAF


class EssentialServiceFactory(factory.DjangoModelFactory):
    """Factory for Essential Services."""

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

    class Meta:
        model = EssentialService

    name = random.choice(fnames)
    description = Faker(
        "paragraph", nb_sentences=4, variable_nb_sentences=True, ext_word_list=None
    )
    organisation = factory.SubFactory(OrganisationFactory)
    caf = factory.SubFactory("ctrack.caf.tests.factories.CAFFactory")


class GradingFactory(factory.DjangoModelFactory):
    descriptor = factory.Iterator(
        ["Q1", "Q2", "Q3", "Q4", "Q5", "C1", "C2", "C3", "C4", "C5"]
    )
    description = Faker("text", max_nb_chars=100, ext_word_list=None)
    type = factory.Iterator(Grading.GRADING_TYPE, getter=lambda g: g[0])

    class Meta:
        model = Grading


class FileStoreFactory(factory.DjangoModelFactory):
    descriptor = "File Store X"
    virtual_location = Faker("street_name")
    physical_location = random.choice(["Cupboard A", "Tin Box", "The Vault"])
    physical_location_organisation = factory.SubFactory(OrganisationFactory)

    class Meta:
        model = FileStore


class DocumentFileFactory(factory.DjangoModelFactory):
    name = Faker("file_name", extension="xlsx")
    type = random.choice([1, 2, 3, 4])
    file_store_location = factory.SubFactory(FileStoreFactory)

    class Meta:
        model = DocumentFile
