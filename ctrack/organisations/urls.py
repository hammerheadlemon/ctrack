from django.urls import path

from ctrack.organisations.forms import OrganisationCreateForm, AddressCreateForm
from ctrack.organisations.views import OrganisationDetailView, OrganisationListView, OrganisationCreate, \
    OrganisationCreateWizard

app_name = "organisations"

urlpatterns = [
    path("<slug:slug>/", view=OrganisationDetailView.as_view(), name="detail"),
    path("add-wizard", view=OrganisationCreateWizard.as_view([OrganisationCreateForm, AddressCreateForm])),
    path("", view=OrganisationListView.as_view(), name="list"),
    path("create", view=OrganisationCreate.as_view(), name="create")
]
