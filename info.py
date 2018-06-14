#
# PHYS 129 final project
# Poisson's Spot
# GUI
#
# June 6, 2018 created by Renjie Zhu
#

import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QErrorMessage,
    QMenuBar,
    QMessageBox,
)
from PyQt5.QtCore import (
    pyqtSlot,
)


class Info(QWidget):
    def __init__(self, left=300, top=300, width=450, height=180, title='New Window'):
        super().__init__()
        self.title = title
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.ok_button = QPushButton('OK', self)
        self.ok_button.move(310, 140)

    def info_window(self, info_text):
        information = QLabel(info_text, self)
        information.move(20, 10)

        credits = QLabel("""
by: 
Zhexing Zhang (algorithm)
Renjie Zhu (GUI)
""", self)
        credits.move(310, 50)

        self.ok_button.clicked.connect(self.ok_on_click)

        self.show()

    @pyqtSlot(name='ok_on_click')
    def ok_on_click(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = Info()
    a.info_window('hello')
    sys.exit(app.exec_())
