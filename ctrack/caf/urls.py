from django.urls import path
from django.views.decorators.cache import cache_page

from ctrack.caf.views import ListCAF, ListApplicableSystem, caf_detail_view, ApplicableSystemDetail, \
    ApplicableSystemCreateFromOrg, applicable_system_create_from_caf

app_name = "caf"

urlpatterns = [
    path("", view=ListCAF.as_view(), name="caf_list"),
    path("applicablesystems", cache_page(60 * 60)(ListApplicableSystem.as_view()), name="es_list"),
    path("applicablesystems/<int:pk>", ApplicableSystemDetail.as_view(), name="ass_detail"),
    path("applicablesystem/<slug:slug>", ApplicableSystemCreateFromOrg.as_view(), name="create_from_org"),
    path("applicablesystem/create-from-caf/<int:caf_id>", applicable_system_create_from_caf, name="as_create_from_caf"),
    path("<int:pk>", caf_detail_view, name="detail")
]
