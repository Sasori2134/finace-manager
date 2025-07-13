import sys
from PyQt5.QtWidgets import QApplication
from login.login_window import LoginWindow
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = LoginWindow()
    ui.show()
    sys.exit(app.exec_())
    