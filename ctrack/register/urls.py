from django.urls import path

from ctrack.register.views import EngagementEventCreate, EngagementEventDelete

app_name = "register"

urlpatterns = [
    path(
        "engagement-event/create/from-org/<slug:slug>", view=EngagementEventCreate.as_view(), name="create",
    ),
    path(
        "engagement-event/delete/<int:pk>/for-org/<slug:slug>", view=EngagementEventDelete.as_view(), name="ee_delete"
    )
]
