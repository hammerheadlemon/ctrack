from django.urls import path

from ctrack.organisations.views import OrganisationDetailView

app_name = "organisations"

urlpatterns = [
    path("<str:name>/", view=OrganisationDetailView, name="detail")
]
