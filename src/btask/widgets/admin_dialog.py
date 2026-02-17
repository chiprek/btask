from textual import on, work
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label

from .add_project_dialog import AddProjectDialog


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
        self.add_project_workflow()

    @work
    async def add_project_workflow(self) -> None:
        from config import BTaskConfig

        from .sidebar import Sidebar

        project_data = await self.app.push_screen_wait(AddProjectDialog())

        if project_data is None:
            return  # handle user cancelling

        config = BTaskConfig()

        existing = config.get_project_by_id(project_data["id"])
        if existing:
            self.app.notify(
                f"Project ID '{project_data['id']}' already exists", severity="error"
            )
            return

        new_project = {
            "name": project_data["name"],
            "id": project_data["id"],
            "archived": False,
            "kits": [],
        }

        config.add_project(new_project)

        sidebar = self.app.query_one(Sidebar)
        sidebar.load_projects()

        self.app.notify(
            f"Workorder '{project_data['name']}' created!", severity="information"
        )

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
