from PySide6.QtWidgets import QMenuBar, QMenu


class Menu():
    def __init__(self, app: "App"):
        self.menubar: QMenuBar = app.menuBar()
        self.menubar.setNativeMenuBar(False)

        self.fileMenu: QMenu = self.menubar.addMenu('File')

        self.fileMenu.addAction(app.actions.createAction)
        self.fileMenu.addAction(app.actions.openAction)
        self.fileMenu.addAction(app.actions.quitAction)
