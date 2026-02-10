from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select


class EditKitDialog(ModalScreen):
    def __init__(self, kit_data: dict):
        super().__init__()
        self.kit_data = kit_data

    def compose(self) -> ComposeResult:
        with Container(id="edit_kit_dialog"):
            yield Label("Edit Kit", id="edit-dialog-title")

            yield Label("Status:")
            yield Select(
                options=[
                    ("Pending", "Pending"),
                    ("In Progress", "In Progress"),
                    ("Complete", "Complete"),
                ],
                id="edit-kit-status",
            )

            yield Label("notes:")
            yield Input(
                placeholder="edit notes",
                value=self.kit_data.get("notes", ""),
                id="edit-notes",
            )

            with Vertical():
                yield Button("Save", variant="primary", id="edit-kit-save")
                yield Button("Cancel", id="edit-kit-cancel")

    def on_mount(self) -> None:
        status_select = self.query_one("#edit-kit-status", Select)
        status_select.value = self.kit_data.get("status", "Pending")

    @on(Button.Pressed, "#edit-kit-save")
    def handle_edit_kit_save(self) -> None:
        # Implement save logic here
        kit_data = {
            "name": self.kit_data.get("name"),
            "status": self.query_one("#edit-kit-status", Select).value,
            "quantity": self.kit_data.get("quantity"),
            "notes": self.query_one("#edit-notes", Input).value,
        }
        if not kit_data["status"].strip():
            self.app.notify(
                "No changes made please fill in all fields", severity="error"
            )
            return

        self.dismiss(kit_data)

    @on(Button.Pressed, "#edit-kit-cancel")
    def handle_edit_kit_cancel(self) -> None:
        self.dismiss(None)
