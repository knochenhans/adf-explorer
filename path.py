from PySide6.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QWidget


class Path():
    def __init__(self, app: "App"):
        self.app: "App" = app

        self.container: QWidget = QWidget(app)
        layout: QHBoxLayout = QHBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)

        label: QLabel = QLabel('Path:', self.container)
        self.pathInput: QLineEdit = QLineEdit(self.container)

        layout.addWidget(label)
        layout.addWidget(self.pathInput)

        self.pathInput.editingFinished.connect(self.pathEnter)
        self.disable()

    def pathWidget(self) -> QWidget:
        return self.container

    def pathEnter(self) -> None:
        try:
            self.app.navigate(self.pathInput.text())
        except Exception:
            self.pathInput.setText(self.app.adf.node)

    def enable(self) -> None:
        self.pathInput.setDisabled(False)

    def disable(self) -> None:
        self.pathInput.setDisabled(True)

    def setText(self, text: str) -> None:
        self.pathInput.setText(text)

    def text(self) -> str:
        return self.pathInput.text()
