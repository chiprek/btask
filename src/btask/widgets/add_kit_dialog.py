from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select


class AddKitDialog(ModalScreen):
    def compose(self) -> ComposeResult:
        with Container(id="add-kit-dialog"):
            yield Label("Add New Kit", id="dialog-title")

            yield Label("Kitname:")
            yield Input(placeholder="e.g, packoff", id="kit-name")

            yield Label("Status:")
            yield Select(
                options=[
                    ("Pending", "Pending"),
                    ("In Progress", "In Progress"),
                    ("Complete", "Complete"),
                ],
                value="Pending",
                id="kit-status",
            )

            yield Label("Quantity:")
            yield Input(placeholder="0", id="kit-quantity")

            yield Label("Notes:")
            yield Input(placeholder="Optional Notes", id="kit-notes")

            with Vertical():
                yield Button("Add Kit", variant="primary", id="submit-kit")
                yield Button("Cancel", id="cancel-kit")

    @on(Button.Pressed, "#submit-kit")
    def handle_submit(self) -> None:
        kit_data = {
            "name": self.query_one("#kit-name", Input).value,
            "status": self.query_one("#kit-status", Select).value,
            "quantity": self.query_one("#kit-quantity", Input).value,
            "notes": self.query_one("#kit-notes", Input).value,
        }

        if not kit_data["name"].strip():
            self.app.notify("Kit name is required", severity="error")
            return
        self.dismiss(kit_data)

    @on(Button.Pressed, "#cancel-kit")
    def handle_cancel(self) -> None:
        self.dismiss(None)
