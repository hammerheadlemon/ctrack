from django.urls import path
from django.views.decorators.cache import cache_page

from ctrack.caf.views import ListCAF, ListApplicableSystem, caf_detail_view, ApplicableSystemDetail

app_name = "caf"

urlpatterns = [
    path("", view=ListCAF.as_view(), name="caf_list"),
    path("applicablesystems", cache_page(60 * 60)(ListApplicableSystem.as_view()), name="es_list"),
    path("applicablesystems/<int:pk>", ApplicableSystemDetail.as_view(), name="ass_detail"),
    path("<int:pk>",  caf_detail_view, name="detail")
]
