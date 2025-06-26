from PySide6.QtGui import QGuiApplication, QAction, QIcon


class Actions():
    def __init__(self, app: "App") -> None:
        self.createAction: QAction = QAction(QIcon('icons/floppy.png'), 'Create', app)
        self.createAction.setShortcut('Ctrl+N')
        self.createAction.triggered.connect(app.createAdf)

        self.openAction: QAction = QAction(QIcon('icons/hdd.png'), 'Open', app)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.triggered.connect(app.openAdf)

        self.relabelAction: QAction = QAction(QIcon('icons/rename.png'), 'Relabel', app)
        self.relabelAction.setShortcut('Relabel')
        self.relabelAction.triggered.connect(app.relabel)

        self.parentAction: QAction = QAction(QIcon('icons/return.png'), 'Parent', app)
        self.parentAction.setShortcut('Backspace')
        self.parentAction.triggered.connect(app.parent)

        self.makeDirAction: QAction = QAction(QIcon('icons/add-folder.png'), 'Make Directory', app)
        self.makeDirAction.setShortcut('Ctrl+Shift+N')
        self.makeDirAction.triggered.connect(app.makeDir)

        self.extractAction: QAction = QAction(QIcon('icons/download.png'), 'Extract', app)
        self.extractAction.setShortcut('Ctrl+D')
        self.extractAction.triggered.connect(app.extract)

        self.insertAction: QAction = QAction(QIcon('icons/upload.png'), 'Insert', app)
        self.insertAction.setShortcut('Ctrl+I')
        self.insertAction.triggered.connect(app.insert)

        self.deleteAction: QAction = QAction(QIcon('icons/remove.png'), 'Delete', app)
        self.deleteAction.setShortcut('Delete')
        self.deleteAction.triggered.connect(app.delete)

        self.quitAction: QAction = QAction(QIcon('icons/exit.png'), 'Quit', app)
        self.quitAction.setShortcut('Ctrl+Q')
        self.quitAction.triggered.connect(QGuiApplication.quit)

        self.disableAdfActions()

    def disableAdfActions(self) -> None:
        self.disableFileActions()

        self.parentAction.setDisabled(True)
        self.relabelAction.setDisabled(True)
        self.makeDirAction.setDisabled(True)
        self.insertAction.setDisabled(True)

    def enableAdfActions(self) -> None:
        self.parentAction.setDisabled(False)
        self.relabelAction.setDisabled(False)
        self.makeDirAction.setDisabled(False)
        self.insertAction.setDisabled(False)

    def disableFileActions(self) -> None:
        self.extractAction.setDisabled(True)
        self.deleteAction.setDisabled(True)

    def enableFileActions(self) -> None:
        self.extractAction.setDisabled(False)
        self.deleteAction.setDisabled(False)
        self.deleteAction.setDisabled(False)
