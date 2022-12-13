from windows_py_files import name
from PyQt6.QtWidgets import QMainWindow


class Name(QMainWindow, name.Ui_Form):
    def __init__(self):
        super(Name, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.save_name)

    def save_name(self):
        pass