from django.urls import path

from ctrack.register.views import (
    EngagementEventCreate,
    EngagementEventCreateFromCaf,
    EngagementEventDelete,
    SingleDateTimeEventCreate,
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
    # path(
    #     "event/create-caf-single-date-event",
    #     view=CAFSingleDateEventView.as_view(),
    #     name="create_caf_single_date_event"
    # )
]
