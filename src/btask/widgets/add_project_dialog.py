from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Label


class AddProjectDialog(ModalScreen):
    """Modal screen to add a new workorder"""
    def compose(self) -> ComposeResult:
        with Container(id="add-project-dialog"):
            yield Label("Add New Workorder", id="add-project-title")
            
            yield Label("Work order name:")
    