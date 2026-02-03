from config import BTaskConfig
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, HorizontalGroup
from textual.widgets import Button, ProgressBar

from .add_kit_dialog import AddKitDialog
from .pin_prompt import PinPrompt


class PD_Menu(Container):
    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Button(label="Add Kit", id="add-kit")
            yield Button(label="Edit Kit", id="edit-kit")
            yield Button(label="Delete Kit", id="view-port-button-delete")

    @on(Button.Pressed, "#add-kit")
    def handle_add_kit_click(self) -> None:
        self.add_kit_workflow()

    @work
    async def add_kit_workflow(self) -> None:
        entered_pin = await self.app.push_screen_wait(PinPrompt())

        if entered_pin is None:
            return

        config = BTaskConfig()
        if not config.verify_admin_pin(entered_pin):
            self.app.notify("Incorrect PIN", severity="error")
            return

        kit_data = await self.app.push_screen_wait(AddKitDialog())
        if kit_data is None:
            return

        self.app.notify(f"Kit '{kit_data['name']}' added!", severity="information")
