import sys
import datetime
import sqlite3
import time
import shutil

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt6.uic import loadUi


# ----------------DATA BASE CONFIG ------------------------

date = str(datetime.date.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))


class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)
        self.uploader.clicked.connect(self.browsefiles)
        self.send.clicked.connect(self.sendfiles)


    def browsefiles(self):
        fname=QFileDialog.getOpenFileName(self, 'Open file', '/')
        self.filename.setText(fname[0])

    def sendfiles(self):
        source = self.filename.text()
        shutil.copy(source, './upload')
        print("Upload realizado com sucesso!!")

    def loginfunction(self):
        connection = sqlite3.connect('database.db')
        c = connection.cursor()
        email = self.email.text()
        password = self.password.text()
        try:
            c.execute("SELECT password FROM dados WHERE login ='{}'".format(email))
            pass_db = c.fetchall()
            connection.close()
        except:
            print("Erro ao validar o login")

        if password == pass_db[0][0]:
            print("Successfully logged in with email: ", email, "and password:", password)
        else:
            print("Dados de login incorretos!")


    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("createacc.ui", self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def createaccfunction(self):
        connection = sqlite3.connect('database.db')
        c = connection.cursor()
        email = self.email.text()
        if self.password.text( )==self.confirmpass.text():
            password =self.password.text()
            login =Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex() +1)
            c.execute('INSERT INTO dados (login, password, datestamp) VALUES (?, ?, ?)',
                  (email, password, date))
            connection.commit()
            print("Successfully created acc with email: ", email, "and password: ", password)
            connection.close()


app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(480)
widget.setFixedHeight(600)
widget.show()
app.exec()
