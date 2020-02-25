from django.contrib import admin

from .models import CAF, CAFFileStore, DocumentFile, Grading, EssentialService


class EssentialServiceListAdmin(admin.ModelAdmin):
    model = EssentialService
    list_display = ["name", "organisation", "caf"]


class EssentialServiceAdmin(admin.StackedInline):
    model = EssentialService
    max_num = 3
    extra = 1


class CAFAdmin(admin.ModelAdmin):
    # TODO - we need the CAF list to show essential services
    #  but this is a many-to-many relationship, so we need to summarise it somehow
    model = CAF
    inlines = [EssentialServiceAdmin]
    list_display = ["owner", "quality_grading", "confidence_grading", "file"]


admin.site.register(CAF, CAFAdmin)
admin.site.register(CAFFileStore)
admin.site.register(DocumentFile)
admin.site.register(Grading)
admin.site.register(EssentialService, EssentialServiceListAdmin)
