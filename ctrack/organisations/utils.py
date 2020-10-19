from django.contrib.auth.models import User
from django.db.models import QuerySet, Q


def filter_private_events(events: QuerySet, user: User):
    """
    Given a QuerySet containing SingleDateTimeEvent objects,
    ensure that any objects whose user==user and private==True
    are filtered out. This supports OrganisationDetailView, which
    lists all events for an organisation but which must hide private
    events for the logged-in user.
    """
    return events.exclude(~Q(user=user) & Q(private=True))
