from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class ConfirmDialog(ModalScreen[bool]):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        with Container(id="confirm-dialog"):
            yield Label(self.message, id="confirm-message")
            with Horizontal():
                yield Button("Yes", variant="error", id="confirm-yes")
                yield Button("No", id="confirm-no")

    @on(Button.Pressed, "#confirm-yes")
    def handle_yes(self) -> None:
        self.dismiss(True)

    @on(Button.Pressed, "#confirm-no")
    def handle_no(self) -> None:
        self.dismiss(False)
