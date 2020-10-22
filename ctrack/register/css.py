from typing import NamedTuple, List

from ctrack.register.models import EventType, EventBase


class TagAttributes(NamedTuple):
    inline_style: str
    id_str: str


class Swimlane:
    def __init__(self, org_name: str, events: List[EventBase]):
        self.events = events
        self.attrs_added = []
        self.org_name = org_name
        self._process_args()

    def tag_attrs(self, event) -> TagAttributes:
        if event.type_descriptor == EventType.CAF_INITIAL_CAF_RECEIVED.name:
            try:
                self.attrs_added.pop(
                    self.attrs_added.index(EventType.CAF_INITIAL_CAF_RECEIVED.name)
                )
            except ValueError:
                pass
            return TagAttributes(
                inline_style=' style="background-color: green; color: white;"',
                id_str="caf-initial-received-event",
            )
        if event.type_descriptor == EventType.CAF_INITIAL_REVIEW_COMPLETE.name:
            try:
                self.attrs_added.pop(
                    self.attrs_added.index(EventType.CAF_INITIAL_REVIEW_COMPLETE.name)
                )
            except ValueError:
                pass
            return TagAttributes(
                inline_style=' style="background-color: green; color: white;"',
                id_str="caf-initial-review-complete-event",
            )

    def table_row_builder(self):
        if len(self.events) == 0:
            raise ValueError("Cannot handle an empty list")
        tmpl = "<td{0}>{1}</td>"
        org = self.events[0].related_caf.organisation.name
        _tds = [
            tmpl.format(self.tag_attrs(e).inline_style, e.type_descriptor)
            for e in self.events
        ]
        empties = [
            tmpl.format("", e)
            for e in self.attrs_added
            if e[:3] == "CAF"
        ]
        tds = "\n".join(_tds)
        empties_strs = "\n".join(empties)
        return "".join(["<tr>\n", f"<td>{org}</td>\n", tds, "\n", empties_strs, "\n", "</tr>"])

    def _process_args(self):
        for v in EventType:
            setattr(self, v.name, None)
            self.attrs_added.append(v.name)
        for e in self.events:
            setattr(self, str(e.type_descriptor), e)

    @property
    def tr(self):
        return self.table_row_builder()
