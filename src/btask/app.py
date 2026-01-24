from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import (
    Footer,
    Header,
)
from total import get_total
from widgets.pd_menu import PD_Menu
from widgets.project_details import ProjectDetails
from widgets.sidebar import Sidebar


class BTaskApp(App[None]):
    CSS_PATH = "btask.css"
    TITLE = "btask"

    BINDINGS = [
        ("w", "toggle_sidebar", "Toggle Sidebar"),
        ("m", "toggle_pd_menu", "toggle menu"),
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
