from django.contrib import admin

from ctrack.assessments.models import CAFSelfAssessment, CAFObjective, CAFPrinciple, CAFContributingOutcome, \
    CAFSelfAssessmentOutcomeScore


class CAFSelfAssessmentAdmin(admin.ModelAdmin):
    model = CAFSelfAssessment


class CAFObjectiveAdmin(admin.ModelAdmin):
    model = CAFObjective


class CAFPrincipleAdmin(admin.ModelAdmin):
    model = CAFPrinciple


class CAFContributingOutcomeAdmin(admin.ModelAdmin):
    model = CAFContributingOutcome


class CAFSelfAssessmentOutcomeScoreAdmin(admin.ModelAdmin):
    model = CAFSelfAssessmentOutcomeScore


admin.site.register(CAFSelfAssessment, CAFSelfAssessmentAdmin)
admin.site.register(CAFObjective, CAFObjectiveAdmin)
admin.site.register(CAFPrinciple, CAFPrincipleAdmin)
admin.site.register(CAFContributingOutcome, CAFContributingOutcomeAdmin)
admin.site.register(CAFSelfAssessmentOutcomeScore, CAFSelfAssessmentOutcomeScoreAdmin)
