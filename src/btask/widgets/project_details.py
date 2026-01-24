from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Label

from .pd_menu import PD_Menu


class ProjectDetails(Container):
    def compose(self) -> ComposeResult:
        with Container(id="view-port"):
            yield Label("Place-holder", id="place-holder")
            with Vertical():
                yield PD_Menu(id="pd-menu", classes="-hidden")
