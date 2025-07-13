from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont

class MoreButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("More", parent)
        self.setMinimumSize(QSize(211, 51))
        self.setMaximumSize(QSize(211, 51))
        self.setObjectName("load_more")

        # Apply style
        self.setStyleSheet("""
        #load_more {
            color: white;
            background-color: rgb(0, 0, 62);
            font-size: 15pt;
            border: 2px solid #c2c2c2;
            border-radius: 10px;
            padding: 5px;
        }
        #load_more:pressed {
            background-color: gray;
        }
        """)