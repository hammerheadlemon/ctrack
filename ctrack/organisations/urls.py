from django.urls import path

from ctrack.organisations.views import OrganisationDetailView

app_name = "organisations"

urlpatterns = [
    path("<slug:slug>/", view=OrganisationDetailView.as_view(), name="detail")
]
