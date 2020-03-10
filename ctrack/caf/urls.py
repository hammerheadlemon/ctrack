from django.urls import path

from ctrack.caf.views import CreateCAF, ListCAF, ListApplicableSystem, DetailCAF

app_name = "caf"

urlpatterns = [
    path("", view=CreateCAF.as_view(), name="create"),
    path("", view=ListCAF.as_view(), name="caf_list"),
    path("applicablesystems", view=ListApplicableSystem.as_view(), name="es_list"),
    path("<int:pk>",  DetailCAF.as_view(), name="detail")
]
