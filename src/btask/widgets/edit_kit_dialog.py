from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select


class EditKitDialog(ModalScreen):
    def compose(self) -> ComposeResult:
        with Container(id="edit_kit_dialog"):
            yield Label("Edit Kit", id="edit-dialog-title")

            yield Label("Status:")
            yield Select(
                options=[
                    ("Pending", "pending"),
                    ("In Progress", "in_progress"),
                    ("Completed", "completed"),
                ],
                value="Pending",
                id="edit-kit-status",
            )

            yield Label("notes:")
            yield Input(placeholder="edit notes", id="edit-notes")

            with Vertical():
                yield Button("Save", id="edit-kit-save")
                yield Button("Cancel", id="edit-kit-cancel")


@on(Button.Pressed, id="edit-kit-save")
def handle_edit_kit_save(self) -> None:
    # Implement save logic here
    kit_data = {
        "status": self.query_one("#edit-kit-status").value,
        "notes": self.query_one("#edit-notes").value,
    }
    if not kit_data["status"].strip() or not kit_data["notes"].strip():
        self.app.notify("No changes made please fill in all fields", severity="error")
        return
    self.dismiss(kit_data)


@on(Button.Pressed, id="edit-kit-cancel")
def handle_edit_kit_cancel(self) -> None:
    self.dismiss(None)
