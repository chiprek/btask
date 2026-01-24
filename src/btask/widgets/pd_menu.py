from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, ProgressBar
from total import get_total


class PD_Menu(Container):
    def compose(self) -> ComposeResult:
        with Container():
            yield Button(label="yes", id="view-port-button")
            with Horizontal():
                yield ProgressBar(total=get_total())
