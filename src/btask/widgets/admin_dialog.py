from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class AdminMenu(ModalScreen):
    """Admin menu for managing work-orders"""

    def compose(self) -> ComposeResult:
        with Container(id="admin-menu-dialog"):
            yield Label("Admin Menu", id="admin-menu-title")

            with Vertical():
                yield Button("Add Project", id="admin-add-project", variant="primary")
                yield Button(
                    "Delete Project", id="admin-delete-project", variant="error"
                )
                yield Button("Archive Project", id="admin-archive-project")
                yield Button("View Archived Projects", id="admin-view-archived")
                yield Button("Close", id="admin-close")

    @on(Button.Pressed, "#admin-add-project")
    def handle_add_project(self) -> None:
        # TODO: Show add project dialog
        self.app.notify("Add project - TODO")

    @on(Button.Pressed, "#admin-delete-project")
    def handle_delete_project(self) -> None:
        # TODO: Delete selected project
        self.app.notify("Delete project - TODO")

    @on(Button.Pressed, "#admin-archive-project")
    def handle_archive_project(self) -> None:
        # TODO: Archive selected project
        self.app.notify("Archive project - TODO")

    @on(Button.Pressed, "#admin-view-archived")
    def handle_view_archived(self) -> None:
        # TODO: Open archived projects screen
        self.app.notify("View archived - TODO")

    @on(Button.Pressed, "#admin-close")
    def handle_close(self) -> None:
        self.dismiss()
