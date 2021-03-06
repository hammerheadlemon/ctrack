from django.contrib import admin

from .models import (
    CAF,
    FileStore,
    DocumentFile,
    Grading,
    ApplicableSystem,
    EssentialService,
)


def get_system_org(obj):
    es = obj.essentialservice_set.first()  # just get the first if there are many
    if es:  # return blank if there are none to copy with current admin template
        return es.organisation.name
    else:
        return ""


get_system_org.short_description = "Organisation"


class EssentialServiceAdmin(admin.ModelAdmin):
    model = EssentialService
    list_display = ["name", "description", "organisation"]


class ApplicableSystemListAdmin(admin.ModelAdmin):
    model = ApplicableSystem
    list_display = ["name", get_system_org, "function"]


# FIXME
# class ApplicableSystemAdmin(admin.StackedInline):
#     model = ApplicableSystem
#     max_num = 3
#     extra = 1


# FIXME - NOT NEEDED
# def get_caf_name(obj):
#     ass = ApplicableSystem.objects.filter(caf=obj).first()
#     return f"{ass.organisation.name}_v{obj.version}"


# FIXME
class CAFAdmin(admin.ModelAdmin):
    model = CAF
    #   inlines = [ApplicableSystemAdmin]


#   list_display = ["quality_grading", "confidence_grading", "file"]


admin.site.register(CAF, CAFAdmin)
admin.site.register(EssentialService, EssentialServiceAdmin)
admin.site.register(FileStore)
admin.site.register(DocumentFile)
admin.site.register(Grading)
admin.site.register(ApplicableSystem, ApplicableSystemListAdmin)
