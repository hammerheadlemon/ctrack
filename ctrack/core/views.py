from django.contrib.auth import get_user_model
from django.shortcuts import render

from ctrack.caf.models import EssentialService, CAF, ApplicableSystem
from ctrack.organisations.models import IncidentReport, Organisation, Person, Submode
from ctrack.organisations.utils import inspectors_for_each_mode
from ctrack.register.models import EngagementEvent, SingleDateTimeEvent


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
        caf_users = get_user_model().objects.all()
        no_orgs = Organisation.objects.count()
        no_people = Person.objects.count()
        no_singledatetime_events = SingleDateTimeEvent.objects.filter(private=False).count()
        no_meetings = SingleDateTimeEvent.objects.filter(type_descriptor="MEETING", private=False).count()
        no_emails = SingleDateTimeEvent.objects.filter(type_descriptor="EMAIL", private=False).count()
        no_phone_calls = SingleDateTimeEvent.objects.filter(type_descriptor="PHONE_CALL", private=False).count()
        no_video_conferences = SingleDateTimeEvent.objects.filter(type_descriptor="VIDEO_CALL", private=False).count()
        no_cafs = CAF.objects.count()
        no_oes = Organisation.objects.filter(oes=True).count()
        no_essential_services = EssentialService.objects.count()
        no_systems = ApplicableSystem.objects.count()
        submodes = Submode.objects.all().order_by("descriptor")
        submode_inspector_dict = inspectors_for_each_mode("lead_inspector")
        submode_deputy_inspector_dict = inspectors_for_each_mode("deputy_lead_inspector")
        context = {
            "no_oes": no_oes,
            "no_orgs": no_orgs,
            "no_people": no_people,
            "no_singledatetime_events": no_singledatetime_events,
            "no_meetings": no_meetings,
            "no_cafs": no_cafs,
            "no_essential_services": no_essential_services,
            "no_systems": no_systems,
            "no_emails": no_emails,
            "no_phone_calls": no_phone_calls,
            "no_video_conferences": no_video_conferences,
            "caf_users": caf_users,
            "submodes": submodes,
            "submode_inspector_dict": submode_inspector_dict,
            "submode_deputy_inspector_dict": submode_deputy_inspector_dict,
        }
        return render(request, "pages/home.html", context)
