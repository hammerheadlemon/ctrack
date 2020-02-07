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
    RANKING_TYPE = [(1, "Triage"), (2, "First Assessment")]
    descriptor = models.CharField(max_length=100)
    type = models.IntegerField(choices=RANKING_TYPE, default=1)

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


class CAF(models.Model):
    owner = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    essential_system = models.CharField(max_length=255, blank=True)
    triage_ranking = models.ForeignKey(Ranking, on_delete=models.CASCADE)
    file = models.ForeignKey(DocumentFile, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        if not self.essential_system:
            return f"Comprehensive CAF for {self.owner}"
        else:
            return f"{self.essential_system} CAF for {self.owner}"

    class Meta:
        verbose_name = "CAF"
