from typing import TYPE_CHECKING

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QMenuBar

if TYPE_CHECKING:
    from app import App


class Menu:
    def __init__(self, app: "App") -> None:
        self.app = app
        self.menubar: QMenuBar = app.menuBar()
        self.menubar.setNativeMenuBar(False)

        self.fileMenu: QMenu = self.menubar.addMenu("File")

        self.fileMenu.addAction(app.actions.createAction)
        self.fileMenu.addAction(app.actions.openAction)

        # Recent Files submenu
        self.recentFilesMenu: QMenu = QMenu("Open Recent", self.fileMenu)
        self.fileMenu.addMenu(self.recentFilesMenu)
        self.recentFilesActions = []
        self.maxRecentFiles = 5
        self.updateRecentFiles([])  # Initialize with empty list

        self.fileMenu.addAction(app.actions.quitAction)

    def updateRecentFiles(self, recent_files: list[str]):
        # Clear old actions
        for action in self.recentFilesActions:
            self.recentFilesMenu.removeAction(action)
        self.recentFilesActions.clear()

        # Add new actions
        for file_path in recent_files[: self.maxRecentFiles]:
            action = QAction(file_path, self.recentFilesMenu)
            action.triggered.connect(
                lambda checked, path=file_path: self.openRecentFile(path)
            )
            self.recentFilesMenu.addAction(action)
            self.recentFilesActions.append(action)

        if not self.recentFilesActions:
            empty_action = QAction("No Recent Files", self.recentFilesMenu)
            empty_action.setEnabled(False)
            self.recentFilesMenu.addAction(empty_action)
            self.recentFilesActions.append(empty_action)

    def openRecentFile(self, file_path: str):
        # Implement how to open a recent file, e.g.:
        self.app.openFile(file_path)
