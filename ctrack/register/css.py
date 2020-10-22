from dataclasses import dataclass
from typing import NamedTuple, List

from ctrack.register.models import EventType, EventBase, CAFSingleDateEvent


class TagAttributes(NamedTuple):
    inline_style: str
    id_str: str


def tag_attrs(event) -> TagAttributes:
    if event.type_descriptor == EventType.CAF_INITIAL_CAF_RECEIVED.name:
        return TagAttributes(
            inline_style='style="background-color: green; color: white;"',
            id_str="caf-initial-received-event",
        )
    if event.type_descriptor == EventType.CAF_INITIAL_REVIEW_COMPLETE.name:
        return TagAttributes(
            inline_style='style="background-color: green; color: white;"',
            id_str="caf-initial-review-complete-event",
        )


template = (
    "<tr>\n"
    "   <td>{0}</td>\n"
    "   {1}\n"
    "   {2}\n"
    "   <td>OES Revisions Submitted</td>\n"
    "   <td>Validation Agreed</td>\n"
    "   <td>Improvement Plan Submitted</td>\n"
    "   <td>Improvement Plan Review</td>\n"
    "</tr>\n"
)


class Swimlane:
    def __init__(self, org_name: str, events: List[EventBase]):
        self.events = events
        self.org_name = org_name
        self.slots = CAFSwimlaneSlots(*events)  # type: CAFSwimlaneSlots

    @property
    def tr(self):
        initial_submitted_str = "".join(
            [
                "<td ",
                tag_attrs(self.slots.initial_submitted).inline_style,
                ">",
                self.slots.initial_submitted.type_descriptor,
                "</td>"
            ]
        )
        revision_completed_str = "".join(
            [
                "<td ",
                tag_attrs(self.slots.reviewed).inline_style,
                ">",
                self.slots.reviewed.type_descriptor,
                "</td>"
            ]
        )
        return template.format(
            self.org_name, initial_submitted_str, revision_completed_str
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
