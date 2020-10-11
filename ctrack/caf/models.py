from django.db import models

from ctrack.caf.managers import ApplicableSystemManager
from ctrack.organisations.models import Organisation, Person
from django.urls.base import reverse

# from ctrack.register.models import EngagementEvent


class Grading(models.Model):
    GRADING_TYPE = [
        ("CONFIDENCE", "Confidence"),
        ("QUALITY", "Quality"),
        ("MISC", "Misc"),
    ]
    descriptor = models.CharField(max_length=2, help_text="Q1, C1, etc")
    description = models.TextField(max_length=250)
    type = models.CharField(
        max_length=20, choices=GRADING_TYPE, help_text="Type of grading"
    )

    def __str__(self):
        return self.descriptor


class FileStore(models.Model):
    descriptor = models.CharField(max_length=100)
    virtual_location = models.CharField(
        max_length=100, help_text="USB, Rosa, email, etc"
    )
    physical_location = models.CharField(
        max_length=100, blank=True, help_text="Cupboard, room, building, etc"
    )  # cupboard, room, building, address
    physical_location_organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.descriptor


class DocumentFile(models.Model):
    FILETYPE_CHOICES = [(1, "Excel"), (2, "Word"), (3, "PDF"), (4, "Hard Copy")]
    name = models.CharField(max_length=255)
    type = models.IntegerField(choices=FILETYPE_CHOICES, default=1)
    file_store_location = models.ForeignKey(FileStore, on_delete=models.CASCADE)


class ApplicableSystem(models.Model):
    def get_sentinel_org():
        """
        We need this so that we can ensure models.SET() is applied with a callable
        to handle when Users are deleted from the system, preventing the Organisation
        objects related to them being deleted also.
        """
        return Organisation.objects.get_or_create(name="DELETED ORGANISATION")[0]

    CRITICAL = "CR"
    IMPORTANT = "IM"
    SYSTEM_CATEGORISATION = (
        (CRITICAL, "Critical"),
        (IMPORTANT, "Important (Legacy use only)"),
    )

    name = models.CharField(max_length=256, help_text="System name assigned by OES")
    function = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        help_text="How the system is relevant to delivering or supporting the "
        "essential service",
    )
    dft_categorisation = models.CharField(
        max_length=2,
        choices=SYSTEM_CATEGORISATION,
        default=CRITICAL,
        verbose_name="DfT Categorisation",
        help_text="Refer to documentation for description of these criteria",
    )
    oes_categorisation = models.CharField(
        max_length=255,
        default="NA",
        verbose_name="OES Categorisation",
        help_text="Categorisation based on OES' own internal prioritisation process.",
    )

    class Meta:
        verbose_name = "NIS System"

    def get_organisation(self):
        ess = self.essentialservice_set.all()
        org_set = [es.organisation for es in ess]
        if len(org_set) > 1:
            breakpoint()
            raise ValueError("Seeking one organisation, got {}.".format(len(org_set)))
        else:
            return org_set[0]

    def get_cafs(self):
        return self.caf_set.all()

    def __str__(self):
        return self.name

    objects = ApplicableSystemManager()


class CAF(models.Model):
    def get_sentinel_org():
        """
        We need this so that we can ensure models.SET() is applied with a callable
        to handle when Users are deleted from the system, preventing the Organisation
        objects related to them being deleted also.
        """
        return Organisation.objects.get_or_create(name="DELETED ORGANISATION")[0]

    quality_grading = models.ForeignKey(
        Grading,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="quality_grading",
    )
    confidence_grading = models.ForeignKey(
        Grading,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="confidence_grading",
    )
    file = models.ForeignKey(
        DocumentFile, on_delete=models.CASCADE, blank=True, null=True
    )
    version = models.CharField(max_length=10, blank=True, null=True)
    organisation = models.ForeignKey(
        Organisation, on_delete=models.SET(get_sentinel_org)
    )
    triage_review_date = models.DateField(blank=True, null=True)
    triage_review_inspector = models.ForeignKey(
        Person, on_delete=models.CASCADE, blank=True, null=True
    )
    systems = models.ManyToManyField(ApplicableSystem)
    comments = models.TextField(max_length=1000)

    class Meta:
        verbose_name = "CAF"

    def get_absolute_url(self):
        return reverse("caf:detail", kwargs={"pk": self.pk})

    def applicable_systems(self):
        """
        Returns a Queryset of objects we can use in our templates.
        """
        return ApplicableSystem.objects.filter(caf=self)

    def sub_mode(self):
        return self.organisation.submode

    def get_assessments(self):
        return self.cafassessment_set.all()

    # REMOVED UNTIL FIXED EVENT SYSTEM
    # def get_events(self):
    #     return EngagementEvent.objects.filter(related_caf=self).all().order_by("-date")

    def __str__(self):
        # Get the organisation and applicable system
        return f"CAF | {self.organisation.name}_v{self.version}"


class EssentialService(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    systems = models.ManyToManyField(ApplicableSystem)

    def __str__(self):
        return self.name
