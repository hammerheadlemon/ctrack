from django.db import models

from ctrack.caf.models import CAF
from ctrack.organisations.models import Person


class CAFSelfAssessment(models.Model):
    """
    These are carried out by an OES as result in, or are associated with a CAF.
    """
    caf = models.ForeignKey(CAF, on_delete=models.CASCADE)
    completer = models.ForeignKey(Person, on_delete=models.CASCADE)
    comments = models.TextField(max_length=500)

    class Meta:
        verbose_name = "CAF Self Assessment"

    def __str__(self):
        return f"CAF Self Assessment for {self.caf.applicable_systems.first().organisation.name} - version {self.caf.version}"


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


class CAFSelfAssessmentOutcomeScore(models.Model):
    """
    Details the assessment for an Outcome, and the baseline assessment.
    Completed by an OES initially, but can be completed by anyone.
    """
    ASSESSMENT_SCORE = (
        ("Achieved", "Achieved"),
        ("Partially Achieved", "Partially Achieved"),
        ("Not Achieved", "Not Achieved"),
    )
    caf_self_assessment = models.ForeignKey(CAFSelfAssessment, on_delete=models.CASCADE)
    caf_contributing_outcome = models.ForeignKey(CAFContributingOutcome, on_delete=models.CASCADE)
    self_assessment_score = models.CharField(max_length=20, choices=ASSESSMENT_SCORE, help_text="Choose an assessment score")
    baseline_assessment_score = models.CharField(max_length=20, choices=ASSESSMENT_SCORE, help_text="Choose an assessment score")

    class Meta:
        verbose_name = "CAF Self Assessment Outcome Score"

    def __str__(self):
        return f"{self.caf_self_assessment} | {self.self_assessment_score}"
