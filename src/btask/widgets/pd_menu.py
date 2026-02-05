from config import BTaskConfig
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, HorizontalGroup
from textual.widgets import Button, ProgressBar

from .add_kit_dialog import AddKitDialog
from .pin_prompt import PinPrompt
from .project_details import ProjectDetails


class PD_Menu(Container):
    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Button(label="Add Kit", id="add-kit")
            yield Button(label="Edit Kit", id="edit-kit")
            yield Button(label="Delete Kit", id="view-port-button-delete")

    @on(Button.Pressed, "#add-kit")
    def handle_add_kit_click(self) -> None:
        self.add_kit_workflow()

    @work
    async def add_kit_workflow(self) -> None:
        entered_pin = await self.app.push_screen_wait(PinPrompt())
        if entered_pin is None:
            return

        config = BTaskConfig()
        if not config.verify_admin_pin(entered_pin):
            self.app.notify("Incorrect PIN", severity="error")
            return

        kit_data = await self.app.push_screen_wait(AddKitDialog())
        if kit_data is None:
            return

        project_details = self.app.query_one(ProjectDetails)
        current_project_id = project_details.current_project_id

        if not current_project_id:
            self.app.notify("No project selected", severity="error")
            return

        project = config.get_project_by_id(current_project_id)
        if not project:
            self.app.notify("Project not found", severity="error")
            return

        if "kits" not in project:
            project["kits"] = []

        project["kits"].append(
            {
                "name": kit_data["name"],
                "status": kit_data["status"],
                "quantity": int(kit_data["quantity"]) if kit_data["quantity"] else 0,
                "notes": kit_data["notes"],
            }
        )

        # Save the updated project
        config.update_project(current_project_id, project)

        # Step 6: Refresh the display
        project_details.refresh_kit_table()

        # Step 7: Success!
        self.app.notify(f"Kit '{kit_data['name']}' added!", severity="information")
