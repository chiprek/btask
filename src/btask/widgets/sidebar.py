from textual.app import ComposeResult
from textual.containers import Container
from textual.message import Message
from textual.widgets import Label, ListItem, ListView

from btask.config import BTaskConfig


class Sidebar(Container):
    TITLE = "Work_Orders"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.projects = []

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

    def load_projects(self) -> None:
        """Load projects from storage and populate ListView"""
        config = BTaskConfig()
        all_projects = config.load_projects()

        self.projects = [p for p in all_projects if not p.get("archived", False)]

        if not self.projects:
            self.projects = [
                {"name": "Wireline Truck Alpha", "id": "wt_alpha", "archived": False},
                {"name": "Wireline Truck Beta", "id": "wt_beta", "archived": False},
                {"name": "Shop Repairs", "id": "shop_repairs", "archived": False},
            ]
            config.save_projects(self.projects)

        project_list = self.query_one("#project-list", ListView)

        project_list.clear()
        for project in self.projects:
            project_list.append(ListItem(Label(project["name"])))

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """When a project is clicked in the list"""
        project_list = self.query_one("#project-list", ListView)
        selected_item = event.item

        all_items = list(project_list.children)
        try:
            selected_index = all_items.index(selected_item)

            if selected_index < len(self.projects):
                project = self.projects[selected_index]
                self.post_message(self.ProjectSelected(project["id"], project["name"]))
        except ValueError:
            pass  # Item not found in list
