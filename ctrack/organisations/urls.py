from django.urls import path

from ctrack.organisations.views import organisations_detail_view

app_name = "organisations"

urlpatterns = [
    path("<str:name>/", view=organisations_detail_view, name="detail")
]
