from dataclasses import dataclass
from typing import NamedTuple, List, Optional

import pytest

from ctrack.register.models import CAFSingleDateEvent, EventType, EventBase

pytestmark = pytest.mark.django_db


class TagAttributes(NamedTuple):
    inline_style: str
    id_str: str


def tag_attrs(event) -> TagAttributes:
    if event.type_descriptor == EventType.CAF_INITIAL_CAF_RECEIVED.name:
        return TagAttributes(
            inline_style="style=\"background-color: green; color: white;\"",
            id_str="caf-initial-received-event",
        )


@pytest.mark.parametrize(
    "e_type,css_str,id_str",
    [
        (
            EventType.CAF_INITIAL_CAF_RECEIVED.name,
            "style=\"background-color: green; color: white;\"",
            "caf-initial-received-event",
        )
    ],
)
def test_can_get_class_string(caf, user, e_type, css_str, id_str):
    event = CAFSingleDateEvent.objects.create(
        type_descriptor=e_type, related_caf=caf, date="2020-10-20", user=user
    )
    assert tag_attrs(event).inline_style == css_str
    assert tag_attrs(event).id_str == id_str


template = ("<tr>\n"
            "   <td>{0}</td>\n"
            "   <td {1}>CAF Initial Submitted</td>\n"
            "   <td>CAF Reviewed</td>\n"
            "   <td>OES Revisions Submitted</td>\n"
            "   <td>Validation Agreed</td>\n"
            "   <td>Improvement Plan Submitted</td>\n"
            "   <td>Improvement Plan Review</td>\n"
            "</tr>\n")


class Swimlane:
    def __init__(self, org_name: str, events: List[EventBase]):
        self.events = events
        self.org_name = org_name
        self.slots = CAFSwimlaneSlots(*events)  # type: CAFSwimlaneSlots

    @property
    def tr(self):
        return template.format(
            self.org_name, tag_attrs(self.slots.initial_submitted).inline_style
        )


@dataclass(frozen=True)
class CAFSwimlaneSlots:
    """
    The pre-compliance stages we expect.
    """

    initial_submitted: CAFSingleDateEvent = None
    reviewed: CAFSingleDateEvent = None
    revisions_submitted: CAFSingleDateEvent = None
    validation_agreed: CAFSingleDateEvent = None
    improvement_plan_submitted: CAFSingleDateEvent = None
    improvement_plan_reviewed: CAFSingleDateEvent = None
    improvement_plan_agreed: CAFSingleDateEvent = None


class _TestEvent(CAFSingleDateEvent):
    def __init__(self, event):
        self.type_descriptor = event


def test_swimlane_slots():
    slots = CAFSwimlaneSlots(
        initial_submitted=_TestEvent("CAF Initial Submitted"),
        # reviewed=_TestEvent("CAF Reviewed"),
        # revisions_submitted=_TestEvent("CAF Revisions Submitted"),
        # validation_agreed=_TestEvent("CAF Validation Agreed"),
        # improvement_plan_submitted=_TestEvent("Improvement Plan Submitted"),
        # improvement_plan_reviewed=_TestEvent("Improvement Plan Reviewed"),
        # improvement_plan_agreed=_TestEvent("Improvement Plan Agreed"),
    )
    assert slots.initial_submitted.type_descriptor == "CAF Initial Submitted"


def test_progress_chart_slots(caf, user):
    accept = ("<tr>\n"
              "   <td>{}</td>\n"
              "   <td style=\"background-color: green; color: white;\">CAF Initial Submitted</td>\n"
              "   <td>CAF Reviewed</td>\n"
              "   <td>OES Revisions Submitted</td>\n"
              "   <td>Validation Agreed</td>\n"
              "   <td>Improvement Plan Submitted</td>\n"
              "   <td>Improvement Plan Review</td>\n"
              "</tr>\n")
    org_name = caf.organisation.name
    caf_initial = CAFSingleDateEvent.objects.create(
        type_descriptor=EventType.CAF_INITIAL_CAF_RECEIVED.name,
        related_caf=caf,
        date="2020-10-20",
        user=user,
    )
    output = Swimlane(org_name, [caf_initial])
    assert output.tr == accept.format(org_name)
