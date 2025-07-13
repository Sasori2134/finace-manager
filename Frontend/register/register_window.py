from PyQt5.QtWidgets import QMainWindow
from register.register import Register
from user_class import User
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
import requests


class Register_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Register()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('./newlogo.png'))

        self.ui.loginbutton.clicked.connect(self.open_login)
        self.ui.createaccbutton.clicked.connect(self.register)


    def register(self):
            if self.ui.password.text() != self.ui.confirmpassword.text():
                self.ui.wentwrong.setText("Password and Confirm Password Does't Match")
            else:
                response = requests.post('http://127.0.0.1:8000/register', json={'username' : self.ui.username.text(), 'password' : self.ui.password.text()})
                if response.status_code == 400:
                    if response.json().get('username'):
                        self.ui.wentwrong.setText(response.json().get('username')[0])
                    elif response.json().get('password'):
                        self.ui.wentwrong.setText(response.json().get('password')[0])
                else:
                    login = requests.post('http://127.0.0.1:8000/api/token/', json={'username' : self.ui.username.text(), 'password' : self.ui.password.text()})
                    user = User(login.json()['access'], login.json()['refresh'])
                    self.open_main(user)

    def open_main(self,user):
        from main_window import main_window
        self.ui = main_window(user)
        self.ui.show()
        self.close()

    def open_login(self):
        from login.login_window import LoginWindow
        self.login = LoginWindow()
        self.login.show()
        self.close()