from django.db import models

from ctrack.caf.models import CAF
from ctrack.organisations.models import Person


class CAFAssessment(models.Model):
    caf = models.ForeignKey(CAF, on_delete=models.CASCADE)
    completer = models.ForeignKey(Person, on_delete=models.CASCADE)
    comments = models.TextField(max_length=500)

    class Meta:
        verbose_name = "CAF Assessment"

    def get_title(self):
        return f"CAF Assessment for {self.caf.organisation.name} - version {self.caf.version}"

    def __str__(self):
        return f"CAF Assessment for {self.caf.organisation.name} - version {self.caf.version}"


class CAFObjective(models.Model):
    """
    One of 4 as set out in the framework...
    """

    name = models.CharField(max_length=100, help_text="e.g. Managing Risk")
    description = models.TextField(max_length=500)
    order_id = models.IntegerField()

    class Meta:
        verbose_name = "CAF Objective"

    def __str__(self):
        return self.name


class CAFPrinciple(models.Model):
    """
    One of 14 as set out in the framework.
    """

    caf_objective = models.ForeignKey(CAFObjective, on_delete=models.CASCADE)
    designation = models.CharField(max_length=5, help_text="e.g. A1, B3, etc")
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    order_id = models.IntegerField()

    class Meta:
        verbose_name = "CAF Principle"

    def __str__(self):
        return ".".join([self.designation, self.title])


class CAFContributingOutcome(models.Model):
    """
    One of the 39 as set out in the framework.
    """

    designation = models.CharField(max_length=5, help_text="e.g. A1.a, B3.c, etc")
    name = models.CharField(max_length=100, help_text="e.g. Board Direction")
    description = models.TextField(max_length=1000)
    principle = models.ForeignKey(CAFPrinciple, on_delete=models.CASCADE)
    order_id = models.IntegerField()

    class Meta:
        verbose_name = "CAF Contributing Outcome"

    def __str__(self):
        return " ".join([self.designation, self.name])


class CAFAssessmentOutcomeScore(models.Model):
    """
    Details the assessment for an Outcome, and the baseline assessment.
    Completed by an OES initially, but can be completed by anyone.
    """

    ASSESSMENT_SCORE = (
        ("Achieved", "Achieved"),
        ("Partially Achieved", "Partially Achieved"),
        ("Not Achieved", "Not Achieved"),
    )
    caf_assessment = models.ForeignKey(
        CAFAssessment, on_delete=models.CASCADE, verbose_name="CAF Assessment"
    )
    caf_contributing_outcome = models.ForeignKey(
        CAFContributingOutcome,
        on_delete=models.CASCADE,
        verbose_name="CAF Contributing Outcome",
    )
    assessment_score = models.CharField(
        max_length=20,
        choices=ASSESSMENT_SCORE,
        help_text="Choose an assessment score",
        verbose_name="Assessment Score",
    )
    baseline_assessment_score = models.CharField(
        max_length=20,
        choices=ASSESSMENT_SCORE,
        help_text="Choose an assessment score",
        verbose_name="Baseline Score",
    )

    class Meta:
        verbose_name = "CAF Assessment Outcome Score"

    def __str__(self):
        return f"{self.caf_contributing_outcome} | {self.caf_assessment} | {self.assessment_score}"


class AchievementLevel(models.Model):
    descriptor = models.CharField(max_length=50)
    colour_description = models.CharField(max_length=100)
    colour_hex = models.CharField(
        max_length=8
    )  # CSS hex code or simple word descriptor

    def __str__(self):
        return f"{self.descriptor}"


class IGP(models.Model):
    achievement_level = models.ForeignKey(AchievementLevel, on_delete=models.CASCADE)
    contributing_outcome = models.ForeignKey(
        CAFContributingOutcome, on_delete=models.CASCADE
    )
    descriptive_text = models.CharField(max_length=2000)

    class Meta:
        verbose_name = "IGP"
