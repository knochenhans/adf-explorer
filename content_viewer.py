import string

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent, QTextCursor
from PySide6.QtWidgets import (
    QDialog,
    QLineEdit,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
    QCheckBox,
)


class ContentViewer(QDialog):
    def __init__(self, parent: QWidget, file_name: str, file_content: str):
        super().__init__(parent)
        self.setWindowTitle(f"Viewing: {file_name}")

        layout = QVBoxLayout(self)

        # Add line edit for quick search
        self.search_edit = QLineEdit(self)
        self.search_edit.setPlaceholderText("Quick search...")
        layout.addWidget(self.search_edit)

        # Add checkbox for filtering
        self.filter_checkbox = QCheckBox(
            "Show only letters/numbers (replace others with whitespace)", self
        )
        layout.addWidget(self.filter_checkbox)

        self.text_browser = QTextBrowser(self)
        
        fixed_font = self.text_browser.font()
        fixed_font.setFamily("Courier New")
        fixed_font.setStyleHint(fixed_font.StyleHint.Monospace)
        self.text_browser.setFont(fixed_font)
        layout.addWidget(self.text_browser)

        self.original_content = "".join(
            c for c in file_content if c in string.printable
        )
        self.update_text_browser()

        self.resize(1024, 600)

        # Connect search
        self.search_edit.textChanged.connect(self.quick_search)
        self.filter_checkbox.stateChanged.connect(self.update_text_browser)

    def update_text_browser(self):
        if self.filter_checkbox.isChecked():
            filtered = "".join(
                c if c.isalnum() or c.isspace() else " " for c in self.original_content
            )
            self.text_browser.setText(filtered)
        else:
            self.text_browser.setText(self.original_content)

    def quick_search(self, text: str) -> None:
        self.text_browser.moveCursor(QTextCursor.MoveOperation.Start)
        found: bool = self.text_browser.find(text)
        if not found and text:
            self.text_browser.moveCursor(QTextCursor.MoveOperation.Start)
            self.text_browser.find(text)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if (
            event.modifiers() == Qt.KeyboardModifier.ControlModifier
            and event.key() == Qt.Key.Key_F
        ):
            self.search_edit.setFocus()
            event.accept()
        else:
            super().keyPressEvent(event)
