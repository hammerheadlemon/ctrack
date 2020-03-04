from django.contrib import admin

from .models import CAF, FileStore, DocumentFile, Grading, ApplicableSystem


class ApplicableSystemListAdmin(admin.ModelAdmin):
    model = ApplicableSystem
    list_display = ["name", "organisation", "caf"]


class ApplicableSystemAdmin(admin.StackedInline):
    model = ApplicableSystem
    max_num = 3
    extra = 1


class CAFAdmin(admin.ModelAdmin):
    # TODO - we need the CAF list to show essential services
    #  but this is a many-to-many relationship, so we need to summarise it somehow
    model = CAF
    inlines = [ApplicableSystemAdmin]
    list_display = ["owner", "quality_grading", "confidence_grading", "file"]


admin.site.register(CAF, CAFAdmin)
admin.site.register(FileStore)
admin.site.register(DocumentFile)
admin.site.register(Grading)
admin.site.register(ApplicableSystem, ApplicableSystemListAdmin)
