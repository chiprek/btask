import json

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label, ListItem, ListView, Log


class Sidebar(Container):
    TITLE = "Work_Orders"

    def compose(self) -> ComposeResult:
        yield Label("Work Orders", id="work-orders")
        yield ListView(ListItem(Label("example")), ListItem(Label("shiiiiiiiiii")))

    def log_to_sidebar(self, msg: str) -> None:
        self.query_one(Log).write_line(msg)
