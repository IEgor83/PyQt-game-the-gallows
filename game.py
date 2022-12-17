import socket
import threading
import ast
import time

from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QStackedWidget, QMessageBox, QVBoxLayout, QPushButton
from windows_view.rules_game import Rules
from windows_view.servers_of_game import Servers
from windows_view.name_in_game import Name
from windows_view.word_of_game import Word
from windows_view.game_play import Game
from windows_py_files import enter

nickname = None
games = {}
game = None
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5070))


class Enter(QMainWindow, enter.Ui_MainWindow):
    def __init__(self):
        super(Enter, self).__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.play)
        self.pushButton_2.clicked.connect(self.show_rules)
        self.pushButton_3.clicked.connect(self.exit)
        self.nm = None

    def play(self):
        if not nickname:
            self.nm = NameMain()
            self.nm.show()
        else:
            print(widget.currentIndex())
            widget.removeWidget(ServersMain())
            widget.addWidget(ServersMain())
            widget.setCurrentIndex(widget.currentIndex() + 2)

    def show_rules(self):
        print(widget.currentIndex())
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.setFixedWidth(850)
        widget.setFixedHeight(650)

    def exit(self):
        app.exit()


class RulesMain(Rules):
    def __init__(self):
        super(RulesMain, self).__init__()

    def enter_the_game(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.setFixedWidth(850)
        widget.setFixedHeight(600)


class ServersMain(Servers):
    def __init__(self):
        super(ServersMain, self).__init__()
        self.group_box_layout = QVBoxLayout()
        y = 30
        for j in games:
            if len(games[j]) == 4:
                self.i = QPushButton(f'{games[j][3]} 1/2')
                self.i.setEnabled(True)
            else:
                self.i = QPushButton(f'{games[j][3]}, {games[j][5]} 2/2')
                self.i.setEnabled(False)
            self.i.clicked.connect(lambda: self.enter_the_game(j))
            self.i.setGeometry(QtCore.QRect(80, y, 161, 41))
            y += 30
            font = QtGui.QFont()
            font.setPointSize(11)
            self.i.setFont(font)
            self.i.setObjectName(games[j][3])
            self.group_box_layout.addWidget(self.i)
        self.group_box_layout.addStretch()
        self.group_box_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.groupBox.setLayout(self.group_box_layout)

    def enter_the_game(self, adr):
        global game
        game = adr
        print(widget.currentIndex())
        client.send(f'connect_{adr}'.encode())
        widget.addWidget(GameMain(games[adr][0], games[adr][1], 'player'))
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedWidth(850)
        widget.setFixedHeight(650)

    def back(self):
        widget.setCurrentIndex(widget.currentIndex() - 2)

    def create_server(self):
        if self.word_window is None:
            self.word_window = WordMain()
        self.word_window.show()

    def update_servers(self):
        global games
        client.send('update_games'.encode())
        games = client.recv(1024).decode()
        games = ast.literal_eval(games)
        widget.addWidget(ServersMain())
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.removeWidget(widget.widget(2))
        print('nice', widget.currentIndex())


class NameMain(Name):
    def __init__(self):
        super(NameMain, self).__init__()

    def save_name(self):
        global nickname
        global games
        nickname = self.lineEdit.text()
        if len(nickname) > 1:
            client.send(nickname.encode())
            games = client.recv(1024).decode()
            print(games)
            games = ast.literal_eval(games)
            self.close()
            widget.addWidget(ServersMain())
            widget.setCurrentIndex(widget.currentIndex() + 2)


class WordMain(Word):
    def __init__(self):
        super(WordMain, self).__init__()

    def ok(self):
        word = self.lineEdit.text()
        description = self.lineEdit_2.text()
        if len(word) > 1 and len(description) > 1:
            self.write(word, description)
            self.close()
            widget.addWidget(GameMain(word, description, 'user'))
            widget.setCurrentIndex(widget.currentIndex() + 1)
            widget.setFixedWidth(850)
            widget.setFixedHeight(650)

    def write(self, word, description):
        global game
        client.send(f'create_{word}_{description}'.encode())
        server_cl = client.recv(1024).decode()
        game = server_cl


class GameMain(Game):
    def __init__(self, word='None', description='', role='player'):
        super(GameMain, self).__init__(word, description, role)
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

    def check_letter(self, num, but):
        global games
        if self.role == 'player':
            client.send(f'click_{num}'.encode())
        but.setEnabled(False)
        indexes = []
        for i, letter in enumerate(self.word.upper(), 0):
            if num == letter:
                indexes.append(i)
        if indexes:
            but.setStyleSheet('QPushButton {background-color: green; color: white}')
            line = self.lineEdit.text().replace('   ', ' / ').split()
            for elem in indexes:
                line[elem] = num
            line = ' '.join(line).replace('/', ' ')
            self.lineEdit.setText(line)
            if not '?' in line:
                client.send(f'game_over'.encode())
                msg = QMessageBox(self)
                msg.setStyleSheet("QLabel{margin-left: -70px}")
                if self.role == 'player':
                    msg.setWindowTitle("Win")
                    msg.setText("Вы выиграли!")
                else:
                    msg.setWindowTitle("Info")
                    msg.setText("Игрок угадал слово")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setStandardButtons(QMessageBox.StandardButton.Cancel)
                button_one = msg.button(QMessageBox.StandardButton.Cancel)
                button_one.setText('Выход')
                btn = msg.exec()
                if btn == QMessageBox.StandardButton.Cancel:
                    client.send(f'stop_{game}'.encode())
                    update_games = client.recv(1024).decode()
                    games = ast.literal_eval(update_games)
                    print(games)
                    widget.removeWidget(widget.widget(2))
                    widget.addWidget(ServersMain())
                    widget.setCurrentIndex(widget.currentIndex() + 1)
                    widget.setFixedWidth(800)
                    widget.setFixedHeight(650)
                    widget.removeWidget(widget.widget(2))
                    print('nice', widget.currentIndex())
        else:
            self.stage += 1
            if self.stage != 5:
                if self.stage != 7:
                    self.scene.addLine(self.picture_stage[self.stage-1],
                                       QPen(Qt.GlobalColor.black, 4, Qt.PenStyle.SolidLine))
                else:
                    self.scene.addEllipse(self.picture_stage[self.stage - 1],
                                       QPen(Qt.GlobalColor.black, 4, Qt.PenStyle.SolidLine))
            else:
                self.scene.addLine(self.picture_stage[self.stage - 1][0],
                                   QPen(Qt.GlobalColor.black, 4, Qt.PenStyle.SolidLine))
                self.scene.addLine(self.picture_stage[self.stage - 1][1],
                                   QPen(Qt.GlobalColor.black, 4, Qt.PenStyle.SolidLine))
            self.label_2.setText(f'Виселица :  {self.stage}/12')
            but.setStyleSheet('QPushButton {background-color: red; color: white}')
            if self.stage == 12:
                client.send(f'game_over'.encode())
                self.lineEdit.setText(' '.join(list(self.word)))
                msg = QMessageBox(self)
                if self.role == 'player':
                    msg.setWindowTitle("Lose")
                    msg.setText("Вы проиграли!")
                else:
                    msg.setWindowTitle("Info")
                    msg.setText("Игрок не угадал слово")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setStandardButtons(QMessageBox.StandardButton.Cancel)
                button_one = msg.button(QMessageBox.StandardButton.Cancel)
                button_one.setText('Выход')
                btn = msg.exec()
                if btn == QMessageBox.StandardButton.Cancel:
                    client.send(f'stop_{game}'.encode())
                    update_games = client.recv(1024).decode()
                    games = ast.literal_eval(update_games)
                    print(games)
                    widget.removeWidget(widget.widget(2))
                    widget.addWidget(ServersMain())
                    widget.setCurrentIndex(widget.currentIndex() + 1)
                    widget.setFixedWidth(800)
                    widget.setFixedHeight(650)
                    widget.removeWidget(widget.widget(2))
                    print('nice', widget.currentIndex())

    def send_message(self):
        if self.lineEdit_2.text() != '':
            message = '_'.join(['message', self.lineEdit_2.text()])
            client.send(message.encode())
            self.lineEdit_2.setText('')

    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode()
                if self.stage == 12 or not '?' in self.lineEdit.text():
                    print('Поток прекращён')
                    break
                if message.startswith('click'):
                    message = message.split('_')[1]
                    for wid in self.widget.children():
                        if isinstance(wid, QPushButton):
                            if wid.text() == message:
                                wid.setEnabled(True)
                                wid.click()
                else:
                    self.textBrowser.append(message)
            except:
                # в случае любой ошибки лочим открытые инпуты и выводим ошибку
                self.lineEdit_2.setText("Error! Reload app")
                self.lineEdit_2.setEnabled(False)
                self.pushButton.setEnabled(False)
                # закрываем клиент
                client.close()
                break


if __name__ == "__main__":
    app = QApplication([])
    widget = QStackedWidget()
    widget.addWidget(Enter())
    widget.addWidget(RulesMain())
    widget.setFixedWidth(850)
    widget.setFixedHeight(600)
    widget.show()
    app.exec()
