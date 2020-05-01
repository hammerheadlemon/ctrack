from django.urls import path

from ctrack.organisations.views import OrganisationDetailView, OrganisationListView, OrganisationCreate, \
    OrganisationCreateWithAddress

app_name = "organisations"

urlpatterns = [
    path("<slug:slug>/", view=OrganisationDetailView.as_view(), name="detail"),
    path("", view=OrganisationListView.as_view(), name="list"),
    path("create", view=OrganisationCreateWithAddress.as_view(), name="create")
    # path("create", view=OrganisationCreate.as_view(), name="create")
]
