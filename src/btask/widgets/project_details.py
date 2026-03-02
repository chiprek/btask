from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import DataTable, Label

from btask.config import BTaskConfig

from .pd_menu import PD_Menu


class ProjectDetails(Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_project_id = None

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

        self.current_project_id = project_id

        # update the name of the menu
        placeholder = self.query_one("#place-holder", Label)
        placeholder.update(f"Project: {project['name']}")

        self.refresh_kit_table()

    def refresh_kit_table(self) -> None:
        if not self.current_project_id:
            return

        config = BTaskConfig()
        project = config.get_project_by_id(self.current_project_id)

        if not project:
            return

        table = self.query_one("#kits-table", DataTable)
        table.clear()

        if not table.columns:
            table.add_columns("Kit Name", "Status", "Quantity", "Notes", "✓")

        kits = project.get("kits", [])

        if kits:
            for kit in kits:
                completed = kit.get("completed", False)
                check_symbol = "✓" if completed else "☐"
                table.add_row(
                    kit.get("name", ""),
                    kit.get("status", ""),
                    str(kit.get("quantity", 0)),
                    kit.get("notes", ""),
                    check_symbol,
                )
        else:
            table.add_row("No kits added", "-", "-", "-", "-")

    @on(DataTable.CellSelected, "#kits-table")
    def handle_cell_selected(self, event: DataTable.CellSelected) -> None:

        if event.coordinate.column != 4:
            return

        if not self.current_project_id:
            return

        config = BTaskConfig()
        project = config.get_project_by_id(self.current_project_id)

        if not project or "kits" not in project:
            return

        row_index = event.coordinate.row

        if row_index >= len(project["kits"]):
            return

        kit = project["kits"][row_index]
        kit["completed"] = not kit.get("completed", False)

        config.update_project(self.current_project_id, project)

        self.refresh_kit_table()

        status = "completed" if kit["completed"] else "incomplete"
        self.app.notify(f"Kit status updated to {status}")
