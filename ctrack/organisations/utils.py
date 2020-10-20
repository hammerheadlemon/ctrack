from typing import Dict, Set

from django.contrib.auth.models import User
from django.db.models import QuerySet, Q

from ctrack.organisations.models import Submode


def filter_private_events(events: QuerySet, user: User):
    """
    Given a QuerySet containing SingleDateTimeEvent objects,
    ensure that any objects whose user==user and private==True
    are filtered out. This supports OrganisationDetailView, which
    lists all events for an organisation but which must hide private
    events for the logged-in user.
    """
    return events.exclude(~Q(user=user) & Q(private=True))


def inspectors_for_each_mode(lead_type="lead_inspector") -> Dict[str, Set[str]]:
    """
    We want to be able to group lead inspectors by submode.
    """
    if lead_type not in ["lead_inspector", "deputy_lead_inspector"]:
        raise ValueError("Can only query for lead_inspector and deputy_lead_inspector attributes.")
    submodes = Submode.objects.all()
    out = {}
    for sm in submodes:
        insp = set()
        orgs = sm.organisation_set.all()
        for org in orgs:
            insp.add(getattr(org, lead_type))
            insp = {x for x in insp if x is not None}
        out[sm.descriptor] = insp
        del insp
    return out
