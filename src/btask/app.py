from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import DataTable, Footer, Header, Label, ListItem, ListView, Log


class Sidebar(Container):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("Work orders")

    def log_to_sidebar(self, msg: str) -> None:
        self.query_one(Log).write_line(msg)


class BTaskApp(App[None]):
    CSS_PATH = "btask.tcss"
    TITLE = "btask"

    BINDINGS = [("crtl+w", "toggle_sidebar", "Toggle Sidebar")]

    def compose(self) -> ComposeResult:
        yield Sidebar(classes="-hidden")
        yield Header()
        yield Footer()

    def action_toggle_sidebar(self) -> None:
        self.query_one(Sidebar).toggle_class("-hidden")
