from django.contrib import admin

from .models import CAF, CAFFileStore, DocumentFile, Ranking
from .models import ConfidenceAssessment
from .models import EssentialService


class EssentialServiceListAdmin(admin.ModelAdmin):
    model = EssentialService
    list_display = ["name", "organisation", "caf"]


class EssentialServiceAdmin(admin.StackedInline):
    model = EssentialService
    max_num = 3
    extra = 1


class CAFAdmin(admin.ModelAdmin):
    model = CAF
    inlines = [EssentialServiceAdmin]
    list_display = ["owner", "triage_ranking", "confidence_assessment", "file"]


admin.site.register(CAF, CAFAdmin)
admin.site.register(CAFFileStore)
admin.site.register(DocumentFile)
admin.site.register(Ranking)
admin.site.register(ConfidenceAssessment)
admin.site.register(EssentialService, EssentialServiceListAdmin)
