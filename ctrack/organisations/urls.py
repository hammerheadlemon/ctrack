from django.urls import path

from ctrack.organisations.views import (
    IncidentReportCreateView,
    OrganisationCreate,
    OrganisationDetailView,
    OrganisationListView,
    PersonListView,
)

app_name = "organisations"

urlpatterns = [
    path("people/", view=PersonListView.as_view(), name="people"),
    path("<slug:slug>/", view=OrganisationDetailView.as_view(), name="detail"),
    path(
        "<slug:slug>/create-incident-report/",
        view=IncidentReportCreateView.as_view(),
        name="create_incident_report",
    ),
    path("", view=OrganisationListView.as_view(), name="list"),
    path("create", view=OrganisationCreate.as_view(), name="create"),
    # path("create", view=OrganisationCreate.as_view(), name="create")
]
