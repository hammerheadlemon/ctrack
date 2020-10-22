from dataclasses import dataclass
from typing import NamedTuple, List

import pytest

from ctrack.register.models import CAFSingleDateEvent, EventType, EventBase

pytestmark = pytest.mark.django_db


class TagAttributes(NamedTuple):
    inline_style: str
    id_str: str


def tag_attrs(event) -> TagAttributes:
    if event.type_descriptor == EventType.CAF_INITIAL_CAF_RECEIVED.name:
        return TagAttributes(
            inline_style="background-color: green; color: white;",
            id_str="caf-initial-received-event",
        )


@pytest.mark.parametrize(
    "e_type,css_str,id_str",
    [
        (
            EventType.CAF_INITIAL_CAF_RECEIVED.name,
            "background-color: green; color: white;",
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


class Swimlane:
    def __init__(self, events: List[EventBase]):
        self.events = events
        self.slots = []


class CAFSwimlaneSlots:
    """
    The pre-compliance stages we expect.
    """

    def __init__(self, events):
        for e in events:
            if e.type_descriptor == "CAF Initial Submitted":
                self._initial_submitted = e
            else:
                self._initial_submitted = None
            if e.type_descriptor == "CAF Reviewed":
                self._reviewed = e
            else:
                self._reviewed = None
            if e.type_descriptor == "CAF Revisions Submitted":
                self._revisions_submitted = e
            else:
                self._revisions_submitted = None
            if e.type_descriptor == "CAF Validation Agreed":
                self._validation_agreed = e
            else:
                self._validation_agreed = None
            if e.type_descriptor == "Improvement Plan Submitted":
                self._improvement_plan_submitted = e
            else:
                self._improvement_plan_submitted = None
            if e.type_descriptor == "Improvement Plan Reviewed":
                self._improvement_plan_reviewed = e
            else:
                self._improvement_plan_reviewed = None
            if e.type_descriptor == "Improvement Plan Agreed":
                self._improvement_plan_agreed = e
            else:
                self._improvement_plan_agreed = None

    @property
    def initial_submitted(self):
        return self._initial_submitted

    @property
    def improvement_plan_agreed(self):
        return self._improvement_plan_agreed


def test_swimlane_slots():
    class _TestEvent:
        def __init__(self, type_descriptor):
            self.type_descriptor = type_descriptor

    slots = CAFSwimlaneSlots(
        [
            _TestEvent("CAF Initial Submitted"),
            _TestEvent("CAF Reviewed"),
            _TestEvent("CAF Revisions Submitted"),
            _TestEvent("CAF Validation Agreed"),
            _TestEvent("Improvement Plan Submitted"),
            _TestEvent("Improvement Plan Reviewed"),
            # _TestEvent("Improvement Plan Agreed")
        ]
    )
    assert slots.initial_submitted.type_descriptor == "CAF Initial Submitted"
    assert slots.improvement_plan_agreed is None


def test_progress_chart_slots(caf, user):
    accept = """
            <tr>
              <td>ORG NAME 1</td>
              <td style="background-color: green; color: white;">CAF Initial Submitted</td>
              <td>CAF Reviewed</td>
              <td>OES Revisions Submitted</td>
              <td>Validation Agreed</td>
              <td>Improvement Plan Submitted</td>
              <td>Improvement Plan Review</td>
            </tr>
            """
    caf_initial = CAFSingleDateEvent.objects.create(
        type_descriptor=EventType.CAF_INITIAL_CAF_RECEIVED.name,
        related_caf=caf,
        date="2020-10-20",
        user=user,
    )
    output = Swimlane([caf_initial])
    assert output.tr == accept
