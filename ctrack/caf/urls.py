from django.urls import path
from django.views.decorators.cache import cache_page

from ctrack.caf.views import CreateCAF, ListCAF, ListApplicableSystem, DetailCAF

app_name = "caf"

urlpatterns = [
    path("", view=CreateCAF.as_view(), name="create"),
    path("", view=ListCAF.as_view(), name="caf_list"),
    path("applicablesystems", cache_page(60 * 60)(ListApplicableSystem.as_view()), name="es_list"),
    path("<int:pk>",  DetailCAF.as_view(), name="detail")
]
