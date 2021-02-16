from main_map import Map

from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt

import sys


class MapWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.map_file = "map.png"
        self.operate_map = Map([37.530887, 55.703118], 0.02, "map")
        uic.loadUi("design.ui", self)
        self.initUi()

    def initUi(self):
        self.map_image.setPixmap(QPixmap("Wait_img.jpg"))
        #self.update_picture()

    def update_picture(self):
        self.map_image.setPixmap(QPixmap("Wait_img.jpg"))
        with open(self.map_file, "wb") as file:
            file.write(self.operate_map.get_picture())
        self.pixmap = QPixmap(self.map_file)
        self.map_image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_PageUp:
            self.operate_map.zoom("zoom_in")
            self.update_picture()
        elif event.key() == Qt.Key_PageDown:
            self.operate_map.zoom("zoom_away")
            self.update_picture()
        elif event.key() == Qt.Key_Down:
            self.operate_map.move("down")
            self.update_picture()
        elif event.key() == Qt.Key_Up:
            self.operate_map.move("up")
            self.update_picture()
        elif event.key() == Qt.Key_Left:
            self.operate_map.move("left")
            self.update_picture()
        elif event.key() == Qt.Key_Right:
            self.operate_map.move("right")
            self.update_picture()
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