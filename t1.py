import os
import sys
#from PySide2 import *
from PyQt6.QtWidgets import (QProgressBar, QWidget, QPushButton, QProgressBar, QVBoxLayout,  QApplication, QDialog, QMainWindow)
from PySide2 import QtCore
from PySide2.QtCore import QThread, Signal, ProgressDialog


class ProgressDialog(QDialog):
    def __init__(self, parent, source, destination):
        QDialog.__init__(self, parent)

        self.resize(300, 50)

        # setting title
        self.setWindowTitle("Python Progress Bar")
        # setting geometry
        self.setGeometry(200, 200, 600, 200)


        self.parent = parent
        self.source = source
        self.destination = destination

        self.prog = QProgressBar(self)
        self.prog.setMaximum(100)
        self.prog.setMinimum(0)
        self.prog.setFormat("%p%")
        self.prog.setGeometry(100, 50, 400, 30)


        self.pushButton = QPushButton(self)
        self.pushButton.setText("Stop!")
        self.pushButton.clicked.connect(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 100, 188, 34))


    def start(self):
        self.show()
        self.copy()

    def copy(self):
        copy_thread = CopyThread(self, self.source, self.destination)
        copy_thread.procPartDone.connect(self.update_progress)
        copy_thread.procDone.connect(self.finished_copy)
        copy_thread.start()


    def update_progress(self, progress):
        self.prog.setValue(progress)

    def finished_copy(self, state):
        print("Upload realizado com sucesso!")

    def centralwidget(self):
        self.close()

class CopyThread(QThread):
    procDone = Signal(bool)
    procPartDone = Signal(int)

    def __init__(self, parent, source: str, destination: str):
        QThread.__init__(self, parent)

        self.source = source
        self.destination = destination

    def run(self):
        self.copy()
        self.procDone.emit(True)

    def copy(self):
        source_size = os.stat(self.source).st_size
        copied = 0

        with open(self.source, "rb") as source, open(self.destination, "wb") as target:
            while True:
                chunk = source.read(1024)
                if not chunk:
                    break

                target.write(chunk)
                copied += len(chunk)

                self.procPartDone.emit(copied * 100 / source_size)


class MainWindow(QMainWindow):
    def __init__(self, parent: object = None) -> None:
        super().__init__(parent)

        self.src = "/home/dcm/login.py"
        self.dest = "/home/dcm/Desktop/Login.py"

        self.btn = QPushButton(self)
        self.btn.setText("Start copy")
        self.btn.clicked.connect(self.run)

        self.setCentralWidget(self.btn)


    def run(self):
        self.prog = ProgressDialog(self, self.src, self.dest)
        self.prog.start()


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()