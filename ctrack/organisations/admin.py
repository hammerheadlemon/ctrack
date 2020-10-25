from django.contrib import admin

from ctrack.caf.models import CAF, EssentialService

from .models import (
    Address,
    AddressType,
    IncidentReport,
    Mode,
    Organisation,
    Person,
    Role,
    Stakeholder,
    Submode,
)


# So we can get the organisation name - a reverse lookup
def get_organisation_name(person):
    return Organisation.objects.filter(person__id=person.id).first().name


def get_first_caf(org):
    return CAF.objects.filter(organisation__id=org.id).first().version


# We need this to ensure the column header in the admin does't read the func name
get_organisation_name.short_description = "Organisation"


class IncidentReportAdmin(admin.ModelAdmin):
    model = IncidentReport
    readonly_fields = ["date_time_incident_reported"]


class AddressTypeAdmin(admin.ModelAdmin):
    pass


class StakeholderAdmin(admin.ModelAdmin):
    model = Stakeholder


class AddressInLine(admin.StackedInline):
    model = Address
    max_num = 3
    extra = 1


class EssentialServiceInline(admin.StackedInline):
    model = EssentialService
    max_num = 3
    extra = 1


class OrganisationAdmin(admin.ModelAdmin):
    inlines = [AddressInLine, EssentialServiceInline]
    list_display = (
        "name",
        "submode",
        "oes",
        "date_updated",
        "lead_inspector",
        "deputy_lead_inspector",
    )


class PersonAdmin(admin.ModelAdmin):
    model = Person
    list_display = [
        "first_name",
        "last_name",
        "job_title",
        get_organisation_name,
        "email",
        "mobile",
    ]


class RoleAdmin(admin.ModelAdmin):
    model = Role


class ModeAdmin(admin.ModelAdmin):
    model = Mode


class SubmodeAdmin(admin.ModelAdmin):
    model = Submode


# Register your models here.
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(AddressType, AddressTypeAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Mode, ModeAdmin)
admin.site.register(Submode, SubmodeAdmin)
admin.site.register(Stakeholder, StakeholderAdmin)
admin.site.register(IncidentReport, IncidentReportAdmin)
