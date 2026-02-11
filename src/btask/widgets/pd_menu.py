from config import BTaskConfig
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Container, HorizontalGroup
from textual.widgets import Button, DataTable

from .add_kit_dialog import AddKitDialog
from .confirm_dialog import ConfirmDialog
from .edit_kit_dialog import EditKitDialog
from .pin_prompt import PinPrompt


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
        from .project_details import ProjectDetails

        # Step 1: Get PIN
        entered_pin = await self.app.push_screen_wait(PinPrompt())
        if entered_pin is None:
            return

        # Step 2: Verify PIN
        config = BTaskConfig()
        if not config.verify_admin_pin(entered_pin):
            self.app.notify("Incorrect PIN", severity="error")
            return

        # Step 3: Show Add Kit dialog
        kit_data = await self.app.push_screen_wait(AddKitDialog())
        if kit_data is None:
            return

        # log(f"Kit data received: {kit_data}")

        # Step 4: Get the current project from ProjectDetails
        project_details = self.app.query_one(ProjectDetails)
        current_project_id = project_details.current_project_id

        # log(f"Current project ID: {current_project_id}")

        if not current_project_id:
            self.app.notify("No project selected", severity="error")
            return

        # Step 5: Load the project, add the kit, save it back
        project = config.get_project_by_id(current_project_id)
        # log(f"Loaded project: {project}")

        if not project:
            self.app.notify("Project not found", severity="error")
            return

        # Ensure kits list exists
        if "kits" not in project:
            project["kits"] = []

        # log(f"Kits before adding: {project['kits']}")

        # Add the new kit
        project["kits"].append(
            {
                "name": kit_data["name"],
                "status": kit_data["status"],
                "quantity": int(kit_data["quantity"]) if kit_data["quantity"] else 0,
                "notes": kit_data["notes"],
                "completed": False,
            }
        )

        # log(f"Kits after adding: {project['kits']}")

        # Save the updated project
        success = config.update_project(current_project_id, project)
        if not success:
            self.app.notify("Failed to save kit", severity="error")
            return
        # log(f"Save successful: {success}")

        # Step 6: Refresh the display
        # log("Calling refresh_kits_table...")
        project_details.refresh_kit_table()
        # log("Refresh complete")

        # Step 7: Success!
        self.app.notify(f"Kit '{kit_data['name']}' added!", severity="information")

    @on(Button.Pressed, "#view-port-button-delete")
    def handle_delete_kit_click(self) -> None:
        self.delete_kit_workflow()

    @work
    async def delete_kit_workflow(self) -> None:
        from .project_details import ProjectDetails

        project_details = self.app.query_one(ProjectDetails)
        current_project_id = project_details.current_project_id

        if not current_project_id:
            self.app.notify("No project selected", severity="error")
            return

        table = self.app.query_one("#kits-table", DataTable)

        if table.cursor_row is None:
            self.app.notify(
                "No kit selected. click on a kit first.", severity="warning"
            )
            return

        selected_row_index = table.cursor_row

        config = BTaskConfig()
        project = config.get_project_by_id(current_project_id)

        if not project or "kits" not in project:
            self.app.notify("Project not found", severity="error")
            return

        if selected_row_index >= len(project["kits"]):
            self.app.notify("Invalid kit selection", severity="error")
            return

        kit_to_delete = project["kits"][selected_row_index]
        kit_name = kit_to_delete.get("name", "Unknown")

        entered_pin = await self.app.push_screen_wait(PinPrompt())
        if entered_pin is None:
            return

        if not config.verify_admin_pin(entered_pin):
            self.app.notify("Incorrect PIN", severity="error")
            return

        confirmed = await self.app.push_screen_wait(
            ConfirmDialog(f"Delete kit '{kit_name}'?")
        )

        if not confirmed:
            return

        del project["kits"][selected_row_index]

        config.update_project(current_project_id, project)

        project_details.refresh_kit_table()

        self.app.notify(f"Kit '{kit_name}' deleted", severity="information")

    @on(Button.Pressed, "#edit-kit")
    def handle_edit_kit_click(self) -> None:
        self.edit_kit_workflow()

    @work
    async def edit_kit_workflow(self) -> None:
        from .project_details import ProjectDetails

        project_details = self.app.query_one(ProjectDetails)
        current_project_id = project_details.current_project_id

        if not current_project_id:
            self.app.notify("No project selected", severity="error")
            return

        table = self.app.query_one("#kits-table", DataTable)

        if table.cursor_row is None:
            self.app.notify(
                "No kit selected. Click on a kit first.", severity="warning"
            )
            return

        selected_row_index = table.cursor_row

        config = BTaskConfig()
        project = config.get_project_by_id(current_project_id)

        if not project or "kits" not in project:
            self.app.notify("Project not found", severity="error")
            return

        if selected_row_index >= len(project["kits"]):
            self.app.notify("Invalid kit selection", severity="error")
            return

        kit_to_edit = project["kits"][selected_row_index]

        kit_data = await self.app.push_screen_wait(EditKitDialog(kit_to_edit))

        if kit_data is None:
            return

        project["kits"][selected_row_index] = {
            "name": kit_data["name"],
            "status": kit_data["status"],
            "quantity": int(kit_data["quantity"]) if kit_data["quantity"] else 0,
            "notes": kit_data["notes"],
            "completed": kit_to_edit.get("completed", False),
        }

        success = config.update_project(current_project_id, project)
        if not success:
            self.app.notify("Failed to update kit", severity="error")
            return

        project_details.refresh_kit_table()

        self.app.notify(f"Kit '{kit_data['name']}' updated!", severity="information")
