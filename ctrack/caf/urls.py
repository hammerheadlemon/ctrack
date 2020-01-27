from django.urls import path

from ctrack.caf.views import CreateCAF

app_name = "caf"

urlpatterns = [
    path("", view=CreateCAF.as_view(), name="create")
]
