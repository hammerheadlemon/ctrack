from django.urls import path

from ctrack.organisations.views import OrganisationDetailView, OrganisationListView, OrganisationCreate, \
    create_org_with_address

app_name = "organisations"

urlpatterns = [
    path("<slug:slug>/", view=OrganisationDetailView.as_view(), name="detail"),
    path("", view=OrganisationListView.as_view(), name="list"),
    path("create", view=create_org_with_address, name="create")
    # path("create", view=OrganisationCreate.as_view(), name="create")
]
