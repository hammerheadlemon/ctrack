from django.urls import path

from ctrack.organisations.views import (
    IncidentReportCreateView,
    OrganisationCreate,
    OrganisationDetailView,
    OrganisationListView,
    PersonListView,
    essential_service_detail,
    person_detail, OrganisationListViewByLeadInspector, oes_list, person_contact_history, )

app_name = "organisations"

urlpatterns = [
    path("oes/", oes_list, name="list_oes"),
    path("people/", view=PersonListView.as_view(), name="people"),
    path("<slug:slug>/", view=OrganisationDetailView.as_view(), name="detail"),
    path(
        "<slug:slug>/create-incident-report/",
        view=IncidentReportCreateView.as_view(),
        name="create_incident_report",
    ),
    path("contact-history-for-person/<int:person_id>", view=person_contact_history, name="person_contact_history"),
    path("", view=OrganisationListView.as_view(), name="list"),
    path("lead-inspector/<int:id>", view=OrganisationListViewByLeadInspector.as_view(), name="list_by_inspector"),
    path("create", view=OrganisationCreate.as_view(), name="create"),
    path(
        "essentialservice/<int:pk>",
        essential_service_detail,
        name="essential_service_detail",
    ),
    path("person/<int:person_id>", person_detail, name="person-detail"),
    # path("create", view=OrganisationCreate.as_view(), name="create")
]
