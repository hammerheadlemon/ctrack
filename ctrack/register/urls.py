from django.urls import path

from ctrack.register.views import EngagementEventCreate, EngagementEventDelete, EngagementEventCreateFromCaf

app_name = "register"

urlpatterns = [
    path(
        "engagement-event/create/from-org/<slug:slug>", view=EngagementEventCreate.as_view(), name="create",
    ),
    path(
        "engagement-event/delete/<int:pk>/for-org/<slug:slug>", view=EngagementEventDelete.as_view(), name="ee_delete"
    ),
    path(
        "engagement-event/create/from-caf/<int:caf_id>", view=EngagementEventCreateFromCaf.as_view(), name="create_from_caf"
    )
]
