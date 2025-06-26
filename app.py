from typing import Dict, List, Optional

from PySide6.QtCore import QMimeData, Qt
from PySide6.QtGui import QDropEvent, QDragEnterEvent
from PySide6.QtWidgets import (
    QFileDialog,
    QInputDialog,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from actions import Actions
from adf import ADF
from browser import Browser
from menu import Menu
from path import Path
from status import Status
from toolbar import Toolbar


class App(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.title: str = "ADF Explorer"
        self.width: int = 640
        self.height: int = 512

        self.adf: ADF = ADF(self)

        self.actions: Actions = Actions(self)
        self.toolbar: Toolbar = Toolbar(self)
        self.menu: Menu = Menu(self)
        self.path: Path = Path(self)
        self.browser: Browser = Browser(self)
        self.status: Status = Status(self)

        self.centralWidget: QWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout: QVBoxLayout = QVBoxLayout(self.centralWidget)

        self.setAcceptDrops(True)  # Enable drag-and-drop

        self.initUI()

    def updateStatusBarMessage(self) -> None:
        self.status.setText()

    def updateWindowTitle(self) -> None:
        if self.adf.volume:
            self.setWindowTitle(self.title + ": " + str(self.adf.volumeName()))
        else:
            self.setWindowTitle(self.title)

    def updatePath(self, path: str) -> None:
        self.path.setText(path)

    def updateBrowser(self, entries: List[Dict[str, str]]) -> None:
        self.browser.populate(entries)

    def parent(self) -> None:
        self.adf.parent()
        self.browser.deselect()

    def navigate(self, path: str) -> None:
        self.adf.navigate(path)
        self.browser.deselect()

    def navigateDown(self, dir: str) -> None:
        self.adf.navigateDown(dir)
        self.browser.deselect()

    def enableFileActions(self) -> None:
        self.actions.enableFileActions()

    def disableFileActions(self) -> None:
        self.actions.disableFileActions()

    def makeDir(self) -> None:
        name, ok = QInputDialog.getText(
            self, "Make Directory", "Please enter a new directory name:"
        )

        if name and ok:
            self.adf.makeDir(name)

    def relabel(self) -> None:
        name, ok = QInputDialog.getText(
            self, "Relabel", "Please enter a new volume name:"
        )

        if name and ok:
            self.adf.relabel(name)

    def delete(self) -> None:
        selected_item = self.browser.selectedItem()
        if not selected_item:
            QMessageBox.warning(self, "No Selection", "No item selected to delete.")
            return

        msgbox = QMessageBox(self)
        msgbox.setIcon(QMessageBox.Icon.Question)
        msgbox.setText(f"Are you sure you want to delete {selected_item}?")
        msgbox.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        result = msgbox.exec()
        if result == QMessageBox.StandardButton.Yes:
            self.adf.delete(selected_item)

    def extract(self) -> None:
        selected_item = self.browser.selectedItem()
        if not selected_item:
            QMessageBox.warning(self, "No Selection", "No item selected to extract.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", ""
        )

        if path:
            self.adf.extract(selected_item, path)

    def insert(self) -> None:
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)

        if dialog.exec_():
            selected_files = dialog.selectedFiles()
            if selected_files:
                self.adf.insert(selected_files[0])

    def createAdf(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Create ADF File",
            "",
            "",
        )

        if path:
            self.adf.create(path)

    def openAdf(self, path: Optional[str] = None) -> None:
        if not path:
            path, _ = QFileDialog.getOpenFileName(
                self,
                "Open ADF File",
                "",
                "",
            )

        if path:
            try:
                self.adf.open(path)
                self.startBrowsing()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open ADF file: {e}")

    def startBrowsing(self, path: str = "/") -> None:
        self.actions.enableAdfActions()
        self.status.setText(self.adf.volumeInfo())
        self.path.enable()
        self.updateWindowTitle()
        self.navigate(path)

    def initUI(self) -> None:
        self.resize(self.width, self.height)
        self.updateWindowTitle()

        # Add components to the layout
        self.layout.addWidget(self.toolbar.toolbar)

        splitter: QSplitter = QSplitter(self.centralWidget)
        splitter.setOrientation(Qt.Orientation.Vertical)
        splitter.addWidget(self.path.pathWidget())
        splitter.addWidget(self.browser.browserWidget())
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)

        self.layout.addWidget(splitter)

        self.show()

    def cleanUp(self) -> None:
        self.adf.cleanUp()

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        mime_data: QMimeData = event.mimeData()
        if mime_data.hasUrls():
            for url in mime_data.urls():
                file_path = url.toLocalFile()
                if file_path.endswith(".adf"):
                    self.openAdf(file_path)
                else:
                    QMessageBox.warning(
                        self, "Invalid File", "Only ADF files are supported."
                    )
