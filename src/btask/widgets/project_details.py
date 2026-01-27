from config import BTaskConfig
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import DataTable, Label

from .pd_menu import PD_Menu


class ProjectDetails(Container):
    def compose(self) -> ComposeResult:
        with Container(id="view-port"):
            yield Label("Project Details", id="place-holder")
            yield DataTable(id="kits-table")
            with Vertical():
                yield PD_Menu(id="pd-menu", classes="-hidden")

    def load_project(self, project_id: str) -> None:
        config = BTaskConfig()
        project = config.get_project_by_id(project_id)

        if not project:
            return
        # update the name of the menu
        placeholder = self.query_one("#place-holder", Label)
        placeholder.update(f"Project: {project['name']}")

        table = self.query_one("#kits-table", DataTable)
        table.clear()

        if not table.columns:
            table.add_columns("Kit Name", "Status", "Quantity", "Notes", "completed")
        kits = project.get("Kits", [])

        if kits:
            for kit in project["kits"]:
                table.add_row(
                    kit.get("name", ""),
                    kit.get("status", ""),
                    str(kit.get("quantity", 0)),
                    kit.get("notes", ""),
                    kit.get("Completed", False),
                )
        else:
            table.add_row("No kits added", "-", "-", "-", "-")
