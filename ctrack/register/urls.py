from django.urls import path

from ctrack.register.views import EngagementEventCreate

app_name = "register"

urlpatterns = [
    path(
        "engagement-event/create/from-org/<slug:slug>", view=EngagementEventCreate.as_view(), name="create"
    ),
]
