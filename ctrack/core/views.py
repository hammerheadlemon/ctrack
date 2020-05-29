from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ctrack.organisations.models import IncidentReport, Organisation


@login_required
def home_page(request):
    if request.user.is_stakeholder:
        org = Organisation.objects.get(
            name=request.user.stakeholder.person.get_organisation_name()
        )
        irs = IncidentReport.objects.filter(organisation=org)
        systems = org.applicablesystem_set.all()
        return render(
            request,
            "pages/stakeholder_home.html",
            context={"org": org, "systems": systems, "irs": irs},
        )
    else:
        return render(request, "pages/home.html")
