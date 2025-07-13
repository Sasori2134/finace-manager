from PyQt5.QtWidgets import QMainWindow
from login.login import Login
from user_class import User
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
import requests

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Login()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('./newlogo.png'))

        self.ui.loginbutton.clicked.connect(self.login)
        self.ui.createacc.clicked.connect(self.open_register)

    def login(self):
        from main_window import main_window
        if not self.ui.username.text():
            self.ui.wentwrong.setText("You Have To Include Username")
        elif not self.ui.password.text():
            self.ui.wentwrong.setText("You Have To Include Password")
        else:
            response = requests.post('http://127.0.0.1:8000/api/token/',json={'username' : self.ui.username.text(), 'password' : self.ui.password.text()})
            if response.status_code == 200:
                user = User(response.json()['access'], response.json()['refresh'])
                self.main = main_window(user)
                self.main.show()
                self.close()
            else:
                self.ui.wentwrong.setText("Wrong Username Or Password")

    def open_register(self):
        from register.register_window import Register_window
        self.register = Register_window()
        self.register.show()
        self.close()