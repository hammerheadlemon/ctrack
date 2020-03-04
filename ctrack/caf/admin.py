from django.contrib import admin

from .models import CAF, FileStore, DocumentFile, Grading, ApplicableSystem


class ApplicableSystemListAdmin(admin.ModelAdmin):
    model = ApplicableSystem
    list_display = ["name", "organisation", "caf"]


class ApplicableSystemAdmin(admin.StackedInline):
    model = ApplicableSystem
    max_num = 3
    extra = 1


def get_caf_name(obj):
    ass = ApplicableSystem.objects.filter(caf=obj).first()
    return f"{ass.organisation.name}_v{obj.version}"


class CAFAdmin(admin.ModelAdmin):
    model = CAF
    inlines = [ApplicableSystemAdmin]
    list_display = [get_caf_name, "quality_grading", "confidence_grading", "file"]


admin.site.register(CAF, CAFAdmin)
admin.site.register(FileStore)
admin.site.register(DocumentFile)
admin.site.register(Grading)
admin.site.register(ApplicableSystem, ApplicableSystemListAdmin)
