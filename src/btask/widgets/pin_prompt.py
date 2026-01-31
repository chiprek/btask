from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label


class PinPrompt(ModalScreen):
    # screen prompt for admin pin

    def compose(self) -> ComposeResult:
        with Container(id="pin-dialog"):
            yield Label("Enter Admin PIN:", id="pin-label")
            yield Input(placeholder="Enter PIN", password=True, id="pin-input")
            yield Button("Submit", variant="primary", id="pin-submit")
            yield Button("Cancel", id="pin-cancel")

    @on(Button.Pressed, "#pin-submit")
    def handle_submit(self) -> None:
        pin_input = self.query_one("#pin-input", Input)
        entered_pin = pin_input.value

        self.dismiss(entered_pin)

    @on(Button.Pressed, "#pin-cancel")
    def handle_cancel(self) -> None:
        self.dismiss(None)
