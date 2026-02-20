from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Select


class DeleteProjectDialog(ModalScreen):
    def __init__(self, projects: list):
        super().__init__()
        self.projects = projects

    def compose(self) -> ComposeResult:
        with Container(id="delete-project-dialog"):
            yield Label("Select a Project to Delete", id="dialog-title")

            yield Label("Project:")
            yield Select(
                options=[(p["name"], p["id"]) for p in self.projects],
                id="project-select",
            )

            with Vertical():
                yield Button("Delete", variant="error", id="confirm-delete")
                yield Button("Cancel", id="cancel-delete")

    @on(Button.Pressed, "#confirm-delete")
    def handle_delete(self) -> None:
        project_id = self.query_one("#project-select", Select).value

        if not project_id:
            self.app.notify("Please select a project", severity="warning")
            return

        self.dismiss(project_id)

    @on(Button.Pressed, "#cancel-delete")
    def handle_cancel(self) -> None:
        self.dismiss(None)
