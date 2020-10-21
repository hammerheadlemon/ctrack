from django.urls import path

from ctrack.compliance.views import overview

app_name = "compliance"

urlpatterns = [
    path("overview", overview, name="overview")
]
