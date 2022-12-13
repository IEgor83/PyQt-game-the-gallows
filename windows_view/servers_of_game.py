import socket
import threading
from windows_py_files import servers
from PyQt6.QtWidgets import QMainWindow, QApplication, QStackedWidget


class Servers(QMainWindow, servers.Ui_MainWindow):
    def __init__(self):
        super(Servers, self).__init__()
        self.setupUi(self)
        self.word_window = None
        self.pushButton_2.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.create_server)

    def back(self):
        pass

    def create_server(self):
        pass
