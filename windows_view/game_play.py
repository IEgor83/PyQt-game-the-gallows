import socket
import threading

from PyQt6.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QMessageBox
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QFont
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, QLineF, QRectF
from windows_py_files import game_window


class Game(QMainWindow, game_window.Ui_MainWindow):
    def __init__(self, word='None'):
        super(Game, self).__init__()
        self.setupUi(self)

        self.word = " ".join('работа'.split())
        self.stage = 0
        s = []
        for i in self.word:
            if i == ' ':
                s.append(i)
            else:
                s.append('?')

        self.lineEdit.setText(' '.join(s))

        self.A_1.clicked.connect(lambda: self.check_letter('А', self.A_1))
        self.A_2.clicked.connect(lambda: self.check_letter('Б', self.A_2))
        self.A_3.clicked.connect(lambda: self.check_letter('В', self.A_3))
        self.A_4.clicked.connect(lambda: self.check_letter('Г', self.A_4))
        self.A_5.clicked.connect(lambda: self.check_letter('Д', self.A_5))
        self.A_6.clicked.connect(lambda: self.check_letter('Е', self.A_6))
        self.A_7.clicked.connect(lambda: self.check_letter('Ё', self.A_7))
        self.A_8.clicked.connect(lambda: self.check_letter('Ж', self.A_8))
        self.A_9.clicked.connect(lambda: self.check_letter('З', self.A_9))
        self.A_10.clicked.connect(lambda: self.check_letter('И', self.A_10))
        self.A_11.clicked.connect(lambda: self.check_letter('Й', self.A_11))
        self.A_12.clicked.connect(lambda: self.check_letter('К', self.A_12))
        self.A_13.clicked.connect(lambda: self.check_letter('Л', self.A_13))
        self.A_14.clicked.connect(lambda: self.check_letter('М', self.A_14))
        self.A_15.clicked.connect(lambda: self.check_letter('Н', self.A_15))
        self.A_16.clicked.connect(lambda: self.check_letter('О', self.A_16))
        self.A_17.clicked.connect(lambda: self.check_letter('П', self.A_17))
        self.A_18.clicked.connect(lambda: self.check_letter('Р', self.A_18))
        self.A_19.clicked.connect(lambda: self.check_letter('С', self.A_19))
        self.A_20.clicked.connect(lambda: self.check_letter('Т', self.A_20))
        self.A_21.clicked.connect(lambda: self.check_letter('У', self.A_21))
        self.A_22.clicked.connect(lambda: self.check_letter('Ф', self.A_22))
        self.A_23.clicked.connect(lambda: self.check_letter('Х', self.A_23))
        self.A_24.clicked.connect(lambda: self.check_letter('Ц', self.A_24))
        self.A_25.clicked.connect(lambda: self.check_letter('Ч', self.A_25))
        self.A_26.clicked.connect(lambda: self.check_letter('Ш', self.A_26))
        self.A_27.clicked.connect(lambda: self.check_letter('Щ', self.A_27))
        self.A_28.clicked.connect(lambda: self.check_letter('Ъ', self.A_28))
        self.A_29.clicked.connect(lambda: self.check_letter('Ы', self.A_29))
        self.A_30.clicked.connect(lambda: self.check_letter('Ь', self.A_30))
        self.A_31.clicked.connect(lambda: self.check_letter('Э', self.A_31))
        self.A_32.clicked.connect(lambda: self.check_letter('Ю', self.A_32))
        self.A_33.clicked.connect(lambda: self.check_letter('Я', self.A_33))

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, 230, 230)
        self.graphicsView.setScene(self.scene)

        self.picture_stage = []
        self.picture_stage.append(QLineF(180, 180, 200, 220))
        self.picture_stage.append(QLineF(180, 180, 180, 220))
        self.picture_stage.append(QLineF(180, 180, 160, 220))
        self.picture_stage.append(QLineF(180, 180, 180, 30))
        self.picture_stage.append((QLineF(180, 30, 80, 30), QLineF(180, 70, 160, 30)))
        self.picture_stage.append(QLineF(90, 30, 90, 50))
        self.picture_stage.append(QRectF(70, 50, 40, 40))
        self.picture_stage.append(QLineF(90, 90, 90, 150))
        self.picture_stage.append(QLineF(90, 90, 70, 120))
        self.picture_stage.append(QLineF(90, 90, 110, 120))
        self.picture_stage.append(QLineF(90, 150, 70, 180))
        self.picture_stage.append(QLineF(90, 150, 110, 180))

    def check_letter(self, num, but):
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
                msg = QMessageBox(self)
                msg.setStyleSheet("QLabel{margin-left: -70px}")
                msg.setWindowTitle("Win")
                msg.setText("Вы выиграли!")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                button_one = msg.button(QMessageBox.StandardButton.Yes)
                button_one.setText('Новая игра')
                button_two = msg.button(QMessageBox.StandardButton.No)
                button_two.setText('Выход')
                btn = msg.exec()
                if btn == QMessageBox.StandardButton.Yes:
                    print("Yes!")
                else:
                    print("No!")
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
                self.lineEdit.setText(' '.join(list(self.word)))
                msg = QMessageBox(self)
                msg.setWindowTitle("Lose")
                msg.setText("Вы проиграли!")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                button_one = msg.button(QMessageBox.StandardButton.Yes)
                button_one.setText('Новая игра')
                button_two = msg.button(QMessageBox.StandardButton.No)
                button_two.setText('Выход')
                btn = msg.exec()
                if btn == QMessageBox.StandardButton.Yes:
                    print("Yes!")
                else:
                    print("No!")


if __name__ == "__main__":
    app = QApplication([])
    window = Game()
    window.show()
    app.exec()
