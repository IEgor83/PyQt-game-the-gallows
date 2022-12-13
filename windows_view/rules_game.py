from windows_py_files import rules
from PyQt6.QtWidgets import QMainWindow


class Rules(QMainWindow, rules.Ui_Form):
    def __init__(self):
        super(Rules, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.enter_the_game)

    def enter_the_game(self):
        pass
