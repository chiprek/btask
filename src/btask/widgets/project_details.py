from config import BTaskConfig
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import DataTable, Label

from .pd_menu import PD_Menu


class ProjectDetails(Container):
    def compose(self) -> ComposeResult:
        with Container(id="view-port"):
            yield Label("Place-holder", id="place-holder")
            yield DataTable(id="kits-table")
            with Vertical():
                yield PD_Menu(id="pd-menu", classes="-hidden")

    def load_project(self, project_id: str) -> None:
        config = BTaskConfig()
        project = config.get_project_by_id(project_id)
        print(f"DEBUG: Found project: {project}")

        if not project:
            print("DEBUG: No project found, returning")
            return
        placeholder = self.query_one("#place-holder", Label)
        placeholder.update(f"Project: {project['name']}")
        print(f"DEBUG: Updated placeholder to: {project['name']}")

        table = self.query_one("#kits-table", DataTable)
        table.clear()
        print("DEBUG: Table cleared")

        if not table.columns:
            table.add_columns("Kit Name", "Status", "Quantity", "Notes")
            print("DEBUG: Columns added")
        kits = project.get("Kits", [])
        print(f"DEBUG: Kits found: {kits}")

        if kits:
            for kit in project["kits"]:
                table.add_row(
                    kit.get("name", ""),
                    kit.get("status", ""),
                    str(kit.get("quantity", 0)),
                    kit.get("notes", ""),
                )
        else:
            print("DEBUG: No kits, adding placeholder row")  # DEBUG
            table.add_row("No kits added", "-", "-", "-")
            print("DEBUG: Placeholder row added")  # DEBUG
