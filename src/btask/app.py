from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import DataTable, Footer, Header, Label, ListItem, ListView, Log


class ProjectDetails(Container):
    def compose(self) -> ComposeResult:
        with DataTable(show_header=True, fixed_rows=10):
            yield Header()


class Sidebar(Container):
    TITLE = "Work_Orders"

    def compose(self) -> ComposeResult:
        yield Label("Work Orders", id="work-orders")
        yield ListView(ListItem(Label("example")), ListItem(Label("shiiiiiiiiii")))

    def log_to_sidebar(self, msg: str) -> None:
        self.query_one(Log).write_line(msg)


class BTaskApp(App[None]):
    CSS_PATH = "btask.tcss"
    TITLE = "btask"

    BINDINGS = [("w", "toggle_sidebar", "Toggle Sidebar")]

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
