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
