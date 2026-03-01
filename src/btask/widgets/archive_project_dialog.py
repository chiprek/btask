from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Select


class ArchiveProjectDialog(ModalScreen):
    def __init__(self, projects: list):
        super().__init__()
        self.projects = projects

    def compose(self) -> ComposeResult:
        with Container(
            id="archive-project-dialog",
        ):
            yield Label("Select a Project to Archive", id="dialog-title")
            yield Select(
                options=[(p["name"], p["id"]) for p in self.projects],
                id="project-select",
            )

        with Vertical():
            yield Button("Archive", variant="error", id="confirm-archive")
            yield Button("Cancel", id="cancel-archive")

    @on(Button.Pressed, "#confirm-archive")
    def handle_archive(self) -> None:
        project_id = self.query_one("#project-select", Select).value

        if not project_id:
            self.app.notify("Please select a project", severity="warning")
            return

        self.dismiss(project_id)

    @on(Button.Pressed, "#cancel-archive")
    def handle_cancel(self) -> None:
        self.dismiss(None)
