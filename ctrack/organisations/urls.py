from django.urls import path

from ctrack.organisations.views import OrganisationDetailView, OrganisationListView

app_name = "organisations"

urlpatterns = [
    path("<slug:slug>/", view=OrganisationDetailView.as_view(), name="detail"),
    path("", view=OrganisationListView.as_view(), name="list")
]
