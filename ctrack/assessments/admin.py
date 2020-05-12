from django.contrib import admin

from ctrack.assessments.models import CAFAssessment, CAFObjective, CAFPrinciple, CAFContributingOutcome, \
    CAFAssessmentOutcomeScore, IGP, AchievementLevel


class CAFAssessmentAdmin(admin.ModelAdmin):
    model = CAFAssessment


class CAFObjectiveAdmin(admin.ModelAdmin):
    model = CAFObjective


class CAFPrincipleAdmin(admin.ModelAdmin):
    model = CAFPrinciple


class CAFContributingOutcomeAdmin(admin.ModelAdmin):
    model = CAFContributingOutcome


class CAFAssessmentOutcomeScoreAdmin(admin.ModelAdmin):
    model = CAFAssessmentOutcomeScore


class IGPAdmin(admin.ModelAdmin):
    model = IGP


class AchievementLevelAdmin(admin.ModelAdmin):
    model = AchievementLevel


admin.site.register(CAFAssessment, CAFAssessmentAdmin)
admin.site.register(CAFObjective, CAFObjectiveAdmin)
admin.site.register(CAFPrinciple, CAFPrincipleAdmin)
admin.site.register(CAFContributingOutcome, CAFContributingOutcomeAdmin)
admin.site.register(CAFAssessmentOutcomeScore, CAFAssessmentOutcomeScoreAdmin)
admin.site.register(IGP, IGPAdmin)
admin.site.register(AchievementLevel, AchievementLevelAdmin)
