from textual.screen import ModalScreen


class ArchiveProjectDialog(ModalScreen):
    def __init__(self, projects: list):
        super().__init__()
        self.projects = projects
