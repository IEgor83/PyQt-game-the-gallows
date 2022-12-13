from windows_py_files import word
from PyQt6.QtWidgets import QMainWindow


class Word(QMainWindow, word.Ui_Form):
    def __init__(self):
        super(Word, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.ok)

    def ok(self):
        pass