from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ctrack.caf.models import EssentialService, CAF, ApplicableSystem
from ctrack.organisations.models import IncidentReport, Organisation, Person
from ctrack.register.models import EngagementEvent


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
        no_orgs = Organisation.objects.count()
        no_people = Person.objects.count()
        no_cafs = CAF.objects.count()
        no_essential_services = EssentialService.objects.count()
        no_systems = ApplicableSystem.objects.count()
        context = {
            "no_orgs": no_orgs,
            "no_people": no_people,
            "no_cafs": no_cafs,
            "no_essential_services": no_essential_services,
            "no_systems": no_systems,
        }
        return render(request, "pages/home.html", context)
