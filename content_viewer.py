import string

from PySide6.QtWidgets import QDialog, QLineEdit, QTextBrowser, QVBoxLayout, QWidget
from PySide6.QtGui import QTextCursor


class ContentViewer(QDialog):
    def __init__(self, parent: QWidget, file_name: str, file_content: str):
        super().__init__(parent)
        self.setWindowTitle(f"Viewing: {file_name}")

        layout = QVBoxLayout(self)

        # Add line edit for quick search
        self.search_edit = QLineEdit(self)
        self.search_edit.setPlaceholderText("Quick search...")
        layout.addWidget(self.search_edit)

        self.text_browser = QTextBrowser(self)
        # Filter content to ASCII only
        ascii_content = ''.join(c for c in file_content if c in string.printable)
        self.text_browser.setText(ascii_content)
        # Set a fixed-width font for hex-like viewing
        fixed_font = self.text_browser.font()
        fixed_font.setFamily("Courier New")
        fixed_font.setStyleHint(fixed_font.StyleHint.Monospace)
        self.text_browser.setFont(fixed_font)
        layout.addWidget(self.text_browser)

        self.resize(1024, 600)

        # Connect search
        self.search_edit.textChanged.connect(self.quick_search)

    def quick_search(self, text: str) -> None:
        self.text_browser.moveCursor(QTextCursor.MoveOperation.Start)
        found: bool = self.text_browser.find(text)
        if not found and text:
            self.text_browser.moveCursor(QTextCursor.MoveOperation.Start)
            self.text_browser.find(text)
