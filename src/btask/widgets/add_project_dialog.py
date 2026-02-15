from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label


class AddProjectDialog(ModalScreen):
    """Modal screen to add a new workorder"""

    def compose(self) -> ComposeResult:
        with Container(id="add-project-dialog"):
            yield Label("Add New Workorder", id="add-project-title")

            yield Label("Work order name:")
            yield Input(placeholder="e.g., Company Name #1234", id="project-name")

            yield Label("Work Order ID:")
            yield Input(placeholder="e.g., 1234", id="project-id")

            with Vertical():
                yield Button(
                    "Create Work Order", variant="primary", id="submit-project"
                )
                yield Button("Cancel", id="cancel-project")

    @on(Button.Pressed, "submit-project")
    def handle_submit(self) -> None:
        project_data = {
            "name": self.query_one("#project-name", Input).value,
            "id": self.query_one("#project-id", Input).value,
        }

        if not project_data["name"].strip():
            self.app.notify("Workorder name is required", severity="error")
            return

        if not project_data["id"].strip():
            self.app.notify("Project ID is required", severity="error")
            return

        self.dismiss(project_data)

    @on(Button.Pressed, "#cancel-project")
    def handle_cancel(self) -> None:
        self.dismiss(None)
