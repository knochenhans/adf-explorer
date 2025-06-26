from typing import TYPE_CHECKING, Dict, List

from PySide6.QtCore import QItemSelection, QModelIndex, Qt
from PySide6.QtGui import QKeyEvent, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QAbstractItemView,
    QListView,
    QStyle,
    QVBoxLayout,
    QWidget,
)

from content_viewer import ContentViewer

if TYPE_CHECKING:
    from app import App


class Browser:
    def __init__(self, app: "App"):
        self.listViewModel: QStandardItemModel = QStandardItemModel()

        self.app: "App" = app

        self.container: QWidget = QWidget(app)
        layout: QVBoxLayout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)

        self.listView: QListView = QListView(self.container)
        self.listView.setModel(self.listViewModel)
        self.listView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.listView.doubleClicked.connect(self.processItem)
        self.listView.keyPressEvent = self.keyPressEvent
        self.listView.selectionModel().selectionChanged.connect(self.selectionChanged)

        layout.addWidget(self.listView)

        self.item: QStandardItem | None = None

    def browserWidget(self) -> QWidget:
        return self.container

    def populate(self, entries: List[Dict[str, str]]) -> None:
        self.listViewModel.clear()

        sorted_entries = sorted(entries, key=lambda e: 0 if e["type"] == "dir" else 1)

        for entry in sorted_entries:
            icon = self.app.style().standardIcon(
                QStyle.StandardPixmap.SP_FileIcon
                if entry["type"] == "file"
                else QStyle.StandardPixmap.SP_DirIcon
            )
            item: QStandardItem = QStandardItem(icon, entry["name"])

            item.setData(entry)
            self.listViewModel.appendRow(item)

    def processItem(self) -> None:
        if self.item and self.item.data()["type"] == "dir":
            self.app.navigateDown(self.selectedItem())
        elif self.item:
            file_name: str = self.selectedItem()
            file_content: str = self.app.adf.extractToMemory(file_name)

            viewer = ContentViewer(self.app, file_name, file_content)
            viewer.exec_()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        QListView.keyPressEvent(self.listView, event)

        if event.key() == Qt.Key.Key_Return:
            self.processItem()

    def deselect(self) -> None:
        self.item = None
        self.app.disableFileActions()

    def selectedItem(self) -> str | None:
        return self.item.text() if self.item else None

    def selectionChanged(
        self, selected: QItemSelection, deselected: QItemSelection
    ) -> None:
        if len(selected.indexes()):
            modelIndex: QModelIndex = selected.indexes()[0]

            self.item = modelIndex.model().item(modelIndex.row())
            self.app.enableFileActions()
        else:
            self.deselect()
