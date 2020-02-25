from django.db import models

from ctrack.organisations.models import Organisation

# TODO - thinking about whether TriageAssessment can be converted into an inherited class
# e.g. we inherit from
# class Assessment(models.Model):
#     descriptor = models.CharField(max_length=100)
#     date_entered = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         abstract = True


class Ranking(models.Model):
    RANKING_TYPE = [(1, "Triage"), (2, "First Assessment"), (3, "Validation")]
    descriptor = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    type = models.IntegerField(choices=RANKING_TYPE, default=1)


    def __str__(self):
        return self.descriptor


class ConfidenceAssessment(models.Model):
    RANKING_TYPE = [("GOOD", "Good"), ("BAD", "Bad"), ("OK", "OK")]
    descriptor = models.CharField(max_length=10, choices=RANKING_TYPE, default=1)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.descriptor


class CAFFileStore(models.Model):
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

    class Meta:
        verbose_name = "CAF File Store"


class DocumentFile(models.Model):
    FILETYPE_CHOICES = [(1, "Excel"), (2, "Word"), (3, "PDF"), (4, "Hard Copy")]
    name = models.CharField(max_length=255)
    type = models.IntegerField(choices=FILETYPE_CHOICES, default=1)
    file_store_location = models.ForeignKey(CAFFileStore, on_delete=models.CASCADE)


class EssentialService(models.Model):
    def get_sentinel_org():
        """
        We need this so that we can ensure models.SET() is applied with a callable
        to handle when Users are deleted from the system, preventing the Organisation
        objects related to them being deleted also.
        """
        return Organisation.objects.get_or_create(name="DELETED ORGANISATION")[0]

    name = models.CharField(max_length=256)
    description = models.TextField(max_length=1000)
    organisation = models.ForeignKey(
        Organisation, on_delete=models.SET(get_sentinel_org)
    )
    caf = models.ForeignKey("CAF", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Essential Service"

    def __str__(self):
        return f"{self.organisation.name} | {self.name}"


class CAF(models.Model):
    owner = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    triage_ranking = models.ForeignKey(Ranking, on_delete=models.CASCADE, blank=True, null=True)
    confidence_assessment = models.ForeignKey(ConfidenceAssessment, on_delete=models.CASCADE, blank=True, null=True)
    file = models.ForeignKey(DocumentFile, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "CAF"

    def __str__(self):
        return f"CAF | {self.owner}"
