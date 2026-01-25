from config import BTaskConfig
from textual.app import ComposeResult
from textual.containers import Container
from textual.message import Message
from textual.widgets import Label, ListItem, ListView, Log


class Sidebar(Container):
    TITLE = "Work_Orders"

    class ProjectSelected(Message):
        def __init__(self, project_id: str, project_name: str):
            self.project_id = project_id
            self.project_name = project_name
            super().__init__()

    def compose(self) -> ComposeResult:
        yield Label("Work Orders", id="work-orders")
        yield ListView(id="project-list")

    def on_mount(self) -> None:
        self.load_projects()
        self.projects = []

    def load_projects(self) -> None:
        config = BTaskConfig()
        projects = config.load_projects()

        if not projects:
            projects = [
                {"name": "SPI #2030", "id": "2030"},
                {"name": "Liberty #2031", "id": "2031"},
                {"name": "Nextier #2032", "id": "2032"},
                {"name": "Tier 1 #2033 ", "id": "2033"},
            ]
            config.save_projects(projects)

        project_list = self.query_one("#project-list", ListView)
        for project in projects:
            project_list.append(ListItem(Label(project["name"])))

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        project_list = self.query_one("#project-list", ListView)
        selected_index = project_list.index

        if selected_index is not None and selected_index < len(self.projects):
            project = self.projects[selected_index]

            self.post_message(self.ProjectSelected(project["id"], project["name"]))

    def log_to_sidebar(self, msg: str) -> None:
        self.query_one(Log).write_line(msg)
