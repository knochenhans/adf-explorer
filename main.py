import sys
from PySide6.QtWidgets import QApplication
from app import App


if __name__ == "__main__":
    qtapp: QApplication = QApplication(sys.argv)
    app: App = App()
    code: int = qtapp.exec()
    app.cleanUp()
    sys.exit(code)
