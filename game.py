import socket
import threading

from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication, QStackedWidget, QMessageBox
from windows_view.rules_game import Rules
from windows_view.servers_of_game import Servers
from windows_view.name_in_game import Name
from windows_view.word_of_game import Word
from windows_py_files import enter

nickname = ''
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5070))

# пишем своё MainWindow, основанное на Ui_MainWindow (которое мы ранее сгенерировали)
class Enter(QMainWindow, enter.Ui_MainWindow):
    def __init__(self):
        # в методе инициализации мы вызываем родительскую инициализацию (устанавливаем элементы интерфейса)
        super(Enter, self).__init__()
        self.setupUi(self)

        # создаем сокет и подключаемся к сокет-серверу
        self.pushButton.clicked.connect(self.play)
        self.pushButton_2.clicked.connect(self.show_rules)
        self.pushButton_3.clicked.connect(self.exit)
        self.nm = None

    def play(self):
        if self.nm is None:
            self.nm = NameMain()
        self.nm.show()

    def show_rules(self):
        widget.setCurrentIndex(widget.currentIndex()+2)
        widget.setFixedWidth(850)
        widget.setFixedHeight(650)

    def exit(self):
        app.exit()


class RulesMain(Rules):
    def enter_the_game(self):
        widget.setCurrentIndex(widget.currentIndex() - 2)
        widget.setFixedWidth(850)
        widget.setFixedHeight(600)


class ServersMain(Servers):
    def back(self):
        print(nickname)
        widget.setCurrentIndex(widget.currentIndex() - 1)

    def create_server(self):
        if self.word_window is None:
            self.word_window = WordMain()
        self.word_window.show()


class NameMain(Name):
    def save_name(self):
        global nickname
        nickname = self.lineEdit.text()
        client.send(nickname.encode('ascii'))
        self.close()
        widget.setCurrentIndex(widget.currentIndex() + 1)


class WordMain(Word):
    def ok(self):
        word = self.lineEdit.text()
        description = self.lineEdit_2.text()
        print(word, description)
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    widget = QStackedWidget()
    widget.addWidget(Enter())
    widget.addWidget(ServersMain())
    widget.addWidget(RulesMain())
    widget.setFixedWidth(850)
    widget.setFixedHeight(600)
    widget.show()
    app.exec()
