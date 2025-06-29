import os
import tempfile
import zipfile
from typing import Dict, List, Optional

from PySide6.QtCore import QMimeData, Qt, QSettings
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QCloseEvent
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
        self.window_width: int = 640
        self.window_height: int = 512

        self.adf: ADF = ADF(self)

        self.app_actions: Actions = Actions(self)
        self.toolbar: Toolbar = Toolbar(self)
        self.menu: Menu = Menu(self)
        self.path: Path = Path(self)
        self.browser: Browser = Browser(self)
        self.status: Status = Status(self)
        self.settings: QSettings = QSettings("ADF Explorer", "ADF Explorer")
        self.menu.loadRecentFiles()

        self.central_widget: QWidget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout: QVBoxLayout = QVBoxLayout(self.central_widget)

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
        self.browser.populate(entries, self.adf.path)

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
        self.app_actions.enableFileActions()

    def disableFileActions(self) -> None:
        self.app_actions.disableFileActions()

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

        path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "")

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
            self.adf.create(path)  # Type: ignore

    def openFile(self, path: Optional[str] = None) -> None:
        if not path:
            path, _ = QFileDialog.getOpenFileName(
                self,
                "Open ADF or ZIP File",
                "",
                "ADF and ZIP Files (*.adf *.zip);;All Files (*)",
            )

        if path:
            try:
                if path.lower().endswith(".zip"):
                    self.openZipAdf(path)
                else:
                    self.adf.open(path)
                    self.startBrowsing()

                self.menu.updateRecentFiles([path])
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file: {e}")

    def startBrowsing(self, path: str = "/") -> None:
        self.app_actions.enableAdfActions()
        self.status.setText(self.adf.volumeInfo())
        self.path.enable()
        self.updateWindowTitle()
        self.navigate(path)

    def initUI(self) -> None:
        self.resize(self.window_width, self.window_height)
        self.updateWindowTitle()

        # Add components to the layout
        self.main_layout.addWidget(self.toolbar.toolbar)

        splitter: QSplitter = QSplitter(self.central_widget)
        splitter.setOrientation(Qt.Orientation.Vertical)
        splitter.addWidget(self.path.pathWidget())
        splitter.addWidget(self.browser.browserWidget())
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)

        self.main_layout.addWidget(splitter)

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
                if file_path.endswith(".adf") or file_path.endswith(".zip"):
                    self.openFile(file_path)
                else:
                    QMessageBox.warning(
                        self, "Invalid File", "Only ADF and ZIP files are supported."
                    )

    def openZipAdf(self, zip_path: str) -> None:
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                adf_files = [
                    name for name in zip_ref.namelist() if name.lower().endswith(".adf")
                ]
                if not adf_files:
                    QMessageBox.critical(
                        self, "Error", "No ADF file found in the ZIP archive."
                    )
                    return
                if len(adf_files) > 1:
                    selected_file, ok = QInputDialog.getItem(
                        self,
                        "Select ADF File",
                        "Multiple ADF files found. Please select one:",
                        adf_files,
                    )
                    if not ok or not selected_file:
                        return
                else:
                    selected_file = adf_files[0]
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = os.path.join(temp_dir, selected_file)
                    zip_ref.extract(selected_file, temp_dir)
                    self.adf.open(temp_path)
                    self.startBrowsing()
        except zipfile.BadZipFile:
            QMessageBox.critical(
                self, "Error", "The selected file is not a valid ZIP archive."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open ZIP file: {e}")

    def closeEvent(self, event: QCloseEvent) -> None:
        self.menu.saveRecentFiles()
        self.cleanUp()
        event.accept()
