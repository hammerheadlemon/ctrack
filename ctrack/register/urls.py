from django.urls import path

from ctrack.register.views import (
    EngagementEventCreate,
    EngagementEventCreateFromCaf,
    EngagementEventDelete,
    SingleDateTimeEventCreate, SingleDateTimeEventUpdate, CreateNoteEvent, CAFCreateSingleDateEventView,
)

app_name = "register"

urlpatterns = [
    path(
        "engagement-event/create/from-org/<slug:slug>",
        view=EngagementEventCreate.as_view(),
        name="create",
    ),
    path(
        "engagement-event/delete/<int:pk>/for-org/<slug:slug>",
        view=EngagementEventDelete.as_view(),
        name="ee_delete",
    ),
    path(
        "engagement-event/create/from-caf/<int:caf_id>",
        view=EngagementEventCreateFromCaf.as_view(),
        name="create_from_caf",
    ),
    path(
        "event/create-simple-event",
        view=SingleDateTimeEventCreate.as_view(),
        name="event_create_simple_event",
    ),
    path(
        "event/update-simple-event/<int:pk>/<slug:org_slug>",
        view=SingleDateTimeEventUpdate.as_view(),
        name="event_update_simple_event_from_org",
    ),
    path(
        "event/create-simple-event-from-org/<slug:org_slug>",
        view=SingleDateTimeEventCreate.as_view(),
        name="event_create_simple_event_from_org",
    ),
    path(
        "event/create-simple-event-from-org/<slug:org_slug>/<str:event_type>",
        view=SingleDateTimeEventCreate.as_view(),
        name="event_create_simple_event_from_org_with_type",
    ),
    path(
        "event/create-note",
        view=CreateNoteEvent.as_view(),
        name="event_create_note"
    ),
    path(
        "event/create-caf-single-date-event/<int:caf_id>",
        view=CAFCreateSingleDateEventView.as_view(),
        name="event_caf_create_single_date_event_from_caf"
    )
    # path(
    #     "event/create-caf-single-date-event",
    #     view=CAFSingleDateEventView.as_view(),
    #     name="create_caf_single_date_event"
    # )
]
