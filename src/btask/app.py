from textual import log, work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import (
    Footer,
    Header,
)
from widgets.project_details import ProjectDetails
from widgets.sidebar import Sidebar


class BTaskApp(App[None]):
    CSS_PATH = "btask.css"
    TITLE = "btask"

    BINDINGS = [
        ("w", "toggle_sidebar", "Toggle Sidebar"),
        ("m", "toggle_pd_menu", "Toggle menu"),
        ("a", "open_admin_menu", "Admin menu"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield Sidebar(
                classes="-hidden",
            )
            with Vertical():
                yield ProjectDetails()
        yield Footer()

    def action_toggle_sidebar(self) -> None:
        self.query_one(Sidebar).toggle_class("-hidden")

    def action_toggle_pd_menu(self) -> None:
        self.query_one("#pd-menu").toggle_class("-hidden")

    def on_sidebar_project_selected(self, message: Sidebar.ProjectSelected) -> None:
        """Handle project selection from sidebar"""
        project_details = self.query_one(ProjectDetails)
        project_details.load_project(message.project_id)

    @work
    async def action_open_admin_menu(self) -> None:
        """Open admin menu after PIN verification"""
        from config import BTaskConfig
        from widgets.admin_dialog import AdminMenu
        from widgets.pin_prompt import PinPrompt

        entered_pin = await self.push_screen_wait(PinPrompt())

        if entered_pin is None:
            return

        config = BTaskConfig()
        if not config.verify_admin_pin(entered_pin):
            log("PIN incorrect")  # Add this
            self.notify("Incorrect PIN", severity="error")
            return

        await self.push_screen(AdminMenu())
