from django.contrib import admin

from ctrack.register.models import EngagementEvent, SingleDateTimeEvent, NoteEvent, CAFSingleDateEvent
from ctrack.register.models import EngagementType


class EngagementEventAdmin(admin.ModelAdmin):
    model = EngagementEvent
    list_display = ("type", "user", "date", "short_description", "response_date_requested")


class EngagementEventTypeAdmin(admin.ModelAdmin):
    model = EngagementEventAdmin
    list_display = ("descriptor", "enforcement_instrument", "single_date_type", "regulation_reference")


class SingleDateTimeEventAdmin(admin.ModelAdmin):
    model = SingleDateTimeEvent
    list_display = ("type_descriptor", "short_description", "date", "user", "created_date")


class CAFSingleDateEventAdmin(admin.ModelAdmin):
    model = CAFSingleDateEvent
    list_display = ("type_descriptor", "date")


class NoteEventAdmin(admin.ModelAdmin):
    model = NoteEvent
    list_display = ("short_description", "organisation", "user")


admin.site.register(EngagementEvent, EngagementEventAdmin)
admin.site.register(EngagementType, EngagementEventTypeAdmin)
admin.site.register(SingleDateTimeEvent, SingleDateTimeEventAdmin)
admin.site.register(CAFSingleDateEvent, CAFSingleDateEventAdmin)
admin.site.register(NoteEvent, NoteEventAdmin)
