from PySide6.QtCore import Qt
from PySide6.QtWidgets import QToolBar


class Toolbar():
    def __init__(self, app: "App"):
        self.toolbar: QToolBar = app.addToolBar('Toolbar')
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.toolbar.addAction(app.actions.createAction)
        self.toolbar.addAction(app.actions.openAction)
        self.toolbar.addAction(app.actions.relabelAction)
        self.toolbar.addAction(app.actions.makeDirAction)
        self.toolbar.addAction(app.actions.parentAction)
        self.toolbar.addAction(app.actions.insertAction)
        self.toolbar.addAction(app.actions.extractAction)
        self.toolbar.addAction(app.actions.deleteAction)
