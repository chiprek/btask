from config import BTaskConfig
from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, HorizontalGroup
from textual.widgets import Button, ProgressBar
from total import get_total

from .pin_prompt import PinPrompt


class PD_Menu(Container):
    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Button(label="Add Kit", id="add-kit")
            yield Button(label="Edit Kit", id="edit=kit")
            yield Button(label="Delete Kit", id="view-port-button-delete")

    @on(Button.Pressed, "#add-Kit")
    async def handle_add_kit(self, event: Button.Pressed) -> None:
        entered_pin = await self.app.push_screen_wait(PinPrompt())

        if entered_pin is None:
            return

        config = BTaskConfig()
        if config.verify_admin_pin(entered_pin):
            self.app.notify("PIN accepted!", severity="information")
        else:
            self.app.notify("Incorrect PIN", severity="error")
