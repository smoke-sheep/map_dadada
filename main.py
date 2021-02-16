from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt

import sys

class MapWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("design.ui", self)
        self.initUi()

    def initUi(self):
        self.map_image.setPixmap(QPixmap("Wait_img.jpg"))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_PageUp:
            pass
        elif event.key() == Qt.Key_PageDown:
            pass
        elif event.key() == Qt.Key_Down:
            pass
        elif event.key() == Qt.Key_Up:
            pass
        elif event.key() == Qt.Key_Left:
            pass
        elif event.key() == Qt.Key_Right:
            pass
        else:
            print(event.key())


def main():
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = MapWidget()
        window.show()
        app.exec_()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()