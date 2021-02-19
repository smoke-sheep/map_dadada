from main_map import Map, ADDRESS_NOT_FOUND
import math
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
        self.operate_map = Map([37.530887, 55.703118], 1, "map")
        uic.loadUi("design.ui", self)
        self.initUi()

    def initUi(self):
        self.map_image.setPixmap(QPixmap("Wait_img.jpg"))

        for i in range(0, 3):
            getattr(self, f"radioButton_{i}").clicked.connect(self.radio_button_clicked)
        self.radioButton_0.setChecked(True)
        self.setFocusPolicy(Qt.WheelFocus)

        self.request_button.clicked.connect(self.line_request)
        self.dump_button.clicked.connect(self.dump_request)

    def line_request(self):
        self.status_label.setText("request address")

        data = self.request_line.text()
        if data != "":
            if self.operate_map.find_adress(data) is not ADDRESS_NOT_FOUND:
                self.update_picture()
            else:
                self.status_label.setText("error in address request")
        else:
            self.status_label.setText("request line is void")

    def dump_request(self):
        self.request_line.setText("")
        self.operate_map.delete_pt()
        self.update_picture()

    def radio_button_clicked(self):
        self.operate_map.change_l(self.sender().text())

    def update_picture(self):
        print("updating picture")
        self.status_label.setText("updating picture")

        self.map_image.setPixmap(QPixmap("Wait_img.jpg"))
        with open(self.map_file, "wb") as file:
            file.write(self.operate_map.get_picture())
        self.pixmap = QPixmap(self.map_file)
        self.map_image.setPixmap(self.pixmap)

        self.status_label.setText("picture is draw")

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

    # pos - координата клика мышки
    def screen_to_geo(self, pos):
        LAT_STEP = 0.008  # Шаги при движении карты по широте и долготе
        LON_STEP = 0.02
        coord_to_geo_x = 0.0000428  # Пропорции пиксельных и географических координат.
        coord_to_geo_y = 0.0000428
        dy = 225 - pos[1]
        dx = pos[0] - 300
        lon = self.operate_map.ll[0]
        lat = self.operate_map.ll[1]
        zoom = self.operate_map.zom
        lx = lon + dx * coord_to_geo_x * math.pow(2, 15 - zoom)
        ly = lat + dy * coord_to_geo_y * math.cos(math.radians(lat)) * math.pow(2, 15 - zoom)
        return lx, ly

    def mouseReleaseEvent(self, event):
        if not 700 > event.x() > 100 and not 550 > event.y() > 100:
            return
        # x = event.x() - 100
        # y = event.y() - 100
        # x_pxls = self.pxls_in_lon()
        # y_pxls = self.pxls_in_lat()
        # ll_0 = [self.operate_map.ll[0] - 300 / x_pxls, self.operate_map.ll[1] - 225 / y_pxls]
        # self.operate_map.find_adress(ll_0[0] + x * x_pxls, ll_0[1] + y * y_pxls, century_map=False)
        # self.update_picture()
        x, y = self.screen_to_geo((event.x() - 100, event.y() - 100))
        # self.operate_map.find_adress(x, y, century_map=False)
        self.operate_map.pt = [x, y]
        self.update_picture()





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