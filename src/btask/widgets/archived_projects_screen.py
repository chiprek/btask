from textual import on, work
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, ListItem, ListView


class ArchivedProjectsScreen(ModalScreen):
    # this will show archived projects with the options to remove archive status if archived in mistake.
    def compose(self) -> ComposeResult:
        with Container(id="archived-projects-screen"):
            yield Label("Archived Projects", id="screen-title")
            yield ListView(id="archived-list")

            with Vertical():
                yield Button(
                    "Unarchive Selected", id="unarchive-project", variant="primary"
                )
                yield Button("Close", id="close-archived")

    def on_mount(self) -> None:
        # load the archived projects on the screen when opened
        self.load_archived_projects()

    def load_archived_projects(self) -> None:
        from config import BTaskConfig

        config = BTaskConfig()
        all_projects = config.load_projects()

        self.archived_projects = [p for p in all_projects if p.get("archived", False)]
        archived_list = self.query_one("#archived-list", ListView)
        archived_list.clear()

        if self.archived_projects:
            for project in self.archived_projects:
                archived_list.append(ListItem(Label(project["name"])))
        else:
            archived_list.append(ListItem(Label("no archived projects")))

    @on(Button.Pressed, "#unarchive-project")
    def handle_unarchive_click(self) -> None:
        self.unarchive_workflow()

    @work
    async def unarchive_workflow(self) -> None:
        # unarchive the selected project

        from config import BTaskConfig

        from .confirm_dialog import ConfirmDialog
        from .sidebar import Sidebar

        archived_list = self.query_one("#archived-list", ListView)

        if archived_list is None:
            self.app.notify("No project selected", severity="warning")
            return

        selected_index = archived_list.index

        if not isinstance(selected_index, int):
            return

        if selected_index >= len(self.archived_projects):
            self.app.notify("Invalid selection", severity="error")
            return

        project = self.archived_projects[selected_index]

        confirmed = await self.app.push_screen_wait(
            ConfirmDialog(f"Unarchive project'{project['name']}'?")
        )
        if not confirmed:
            # user canceled
            return

        config = BTaskConfig()
        success = config.unarchive_project(project["id"])

        if not success:
            self.app.notify("failed to unarchive project", severity="error")
            return

        self.load_archived_projects()

        sidebar = self.app.query_one(Sidebar)
        sidebar.load_projects()

        self.app.notify(
            f"project '{project['name']}' unarchived", severity="information"
        )

    @on(Button.Pressed, "#close-archived")
    def handle_close(self) -> None:
        self.dismiss()
