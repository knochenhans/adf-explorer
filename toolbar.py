from typing import TYPE_CHECKING
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QToolBar

if TYPE_CHECKING:
    from app import App

class Toolbar():
    def __init__(self, app: "App"):
        self.toolbar: QToolBar = app.addToolBar('Toolbar')
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.toolbar.addAction(app.app_actions.createAction)
        self.toolbar.addAction(app.app_actions.openAction)
        self.toolbar.addAction(app.app_actions.relabelAction)
        self.toolbar.addAction(app.app_actions.makeDirAction)
        self.toolbar.addAction(app.app_actions.parentAction)
        self.toolbar.addAction(app.app_actions.insertAction)
        self.toolbar.addAction(app.app_actions.extractAction)
        self.toolbar.addAction(app.app_actions.deleteAction)
