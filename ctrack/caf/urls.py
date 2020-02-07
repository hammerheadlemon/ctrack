from django.urls import path

from ctrack.caf.views import CreateCAF, ListCAF

app_name = "caf"

urlpatterns = [
    path("", view=CreateCAF.as_view(), name="create"),
    path("", view=ListCAF.as_view(), name="caf_list"),
]
