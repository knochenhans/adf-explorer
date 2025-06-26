from PySide6.QtWidgets import QLabel, QStatusBar


class Status():
    def __init__(self, app: "App"):
        self.statusBarMessage: QLabel = QLabel()
        self.statusBarMessage.setText('No file open')

        self.statusBar: QStatusBar = QStatusBar()
        self.statusBar.addWidget(self.statusBarMessage)

        app.setStatusBar(self.statusBar)

    def setText(self, text: str) -> None:
        self.statusBarMessage.setText(text)
