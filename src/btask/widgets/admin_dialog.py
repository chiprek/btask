from textual import on, work
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, DataTable, Label

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
        self.delete_project_workflow()

    @work
    async def delete_project_workflow(self) -> None:
        from config import BTaskConfig

        from .confirm_dialog import ConfirmDialog
        from .delete_project_dialog import DeleteProjectDialog
        from .project_details import ProjectDetails
        from .sidebar import Sidebar

        config = BTaskConfig()

        all_projects = [
            p for p in config.load_projects() if not p.get("archived", False)
        ]

        if not all_projects:
            self.app.notify("No projects to delete", severity="warning")
            return

        selected_project_id = await self.app.push_screen_wait(
            DeleteProjectDialog(all_projects)
        )

        if selected_project_id is None:
            return

        project = config.get_project_by_id(selected_project_id)

        if not project:
            self.app.notify("Project not found", severity="error")
            return

        project_name = project.get("name")
        kits = project.get("kits", [])

        if len(kits) == 0:
            message = f"delete empty project '{project_name}'?"
        else:
            message = f"This project has {len(kits)} kit(s). Delete '{project_name}' and all its kits?"

        confirmed = await self.app.push_screen_wait(ConfirmDialog(message))

        if not confirmed:
            return

        success = config.delete_project(selected_project_id)

        if not success:
            self.app.notify("Failed to delete project", severity="error")

        project_details = self.app.query_one(ProjectDetails)
        if project_details.current_project_id == selected_project_id:
            project_details.current_project_id = None
            table = project_details.query_one("#kits-table", DataTable)
            table.clear()
            placeholder = project_details.query_one("#place-holder", Label)
            placeholder.update("Select a project")

        sidebar = self.app.query_one(Sidebar)
        sidebar.load_projects()

        self.app.notify(f"Project '{project_name}' deleted", severity="information")

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
