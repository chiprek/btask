from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select


class AdminDialog(ModalScreen):
    def compose(self) -> ComposeResult:
        with Container():
            yield Button()
