import random

import factory
from factory import Faker

from ctrack.caf.models import ApplicableSystem, Grading, DocumentFile, FileStore, CAF
from ctrack.organisations.tests.factories import OrganisationFactory, PersonFactory


class CAFFactory(factory.django.DjangoModelFactory):
    quality_grading = factory.SubFactory("ctrack.caf.tests.factories.GradingFactory")
    confidence_grading = factory.SubFactory("ctrack.caf.tests.factories.GradingFactory")
    organisation = factory.SubFactory("ctrack.organisations.tests.OrganisationFactory")
    file = None
    version = Faker("bothify", text="??##", letters="ABCD")
    triage_review_date = Faker("date_object")
    triage_review_inspector = factory.SubFactory(PersonFactory)
    comments = Faker(
        "paragraph", nb_sentences=5, variable_nb_sentences=True, ext_word_list=None
    )

    class Meta:
        model = CAF


class ApplicableSystemFactory(factory.django.DjangoModelFactory):
    """Factory for Essential Services."""

    name = Faker("text", max_nb_chars=100, ext_word_list=None)
    function = Faker(
        "paragraph", nb_sentences=4, variable_nb_sentences=True, ext_word_list=None
    )
    dft_categorisation = "CR"

    class Meta:
        model = ApplicableSystem


class GradingFactory(factory.django.DjangoModelFactory):
    descriptor = factory.Iterator(
        ["Q1", "Q2", "Q3", "Q4", "Q5", "C1", "C2", "C3", "C4", "C5"]
    )
    description = Faker("text", max_nb_chars=100, ext_word_list=None)
    type = factory.Iterator(Grading.GRADING_TYPE, getter=lambda g: g[0])

    class Meta:
        model = Grading


class FileStoreFactory(factory.django.DjangoModelFactory):
    descriptor = "File Store X"
    virtual_location = Faker("street_name")
    physical_location = random.choice(["Cupboard A", "Tin Box", "The Vault"])
    physical_location_organisation = factory.SubFactory(OrganisationFactory)

    class Meta:
        model = FileStore


class DocumentFileFactory(factory.django.DjangoModelFactory):
    name = Faker("file_name", extension="xlsx")
    type = random.choice([1, 2, 3, 4])
    file_store_location = factory.SubFactory(FileStoreFactory)

    class Meta:
        model = DocumentFile
