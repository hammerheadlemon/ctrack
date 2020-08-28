from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ctrack.organisations.models import IncidentReport, Organisation
from ctrack.register.models import EngagementEvent


@login_required
def home_page(request):
    if request.user.is_stakeholder:
        org = Organisation.objects.get(
            name=request.user.stakeholder.person.get_organisation_name()
        )
        irs = IncidentReport.objects.filter(organisation__name=org)
        systems = org.applicable_systems()
        peoples = org.person_set.all()
        engagement_events = EngagementEvent.objects.filter(participants__in=peoples)
        return render(
            request,
            "pages/stakeholder_home.html",
            context={
                "org": org,
                "systems": systems,
                "irs": irs,
                "engagement_events": engagement_events,
            },
        )
    else:
        return render(request, "pages/home.html")
