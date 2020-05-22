from django.urls import path

from ctrack.core.views import home_page

app_name = "core"

urlpatterns = [
    path("", home_page, name="home")
]
