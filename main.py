from basicDetails import *
from main_map import Map, ADDRESS_NOT_FOUND
from mapStream import mapStream
import math
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
from business import *
import sys
import os

INDEX_NOT_SHOW = False
INDEX_SHOW = True


class MapWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.operate_map = Map([37.530887, 55.703118], 10, "map")
        self.address = self.operate_map.formatted_address('37.530887,55.703118')
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

        self.index_show_status = INDEX_NOT_SHOW
        self.index_checkBox.stateChanged.connect(self.change_index_show_status)

        self.thread = QtCore.QThread()  # создаем поток
        self.mapStream = mapStream()
        self.mapStream.moveToThread(self.thread)
        self.mapStream.newImage.connect(self.print_image)  # подключаем события
        self.mapStream.newAddress.connect(self.print_address)
        self.mapStream.mapError.connect(self.map_error)
        self.thread.started.connect(self.mapStream.run)
        self.thread.start()  # запустим поток
        self.update_picture()

    @QtCore.pyqtSlot(str)
    def map_error(self, data):
        print(data)

    @QtCore.pyqtSlot(str)
    def print_address(self, data):
        self.full_address_line.setText(data)

    @QtCore.pyqtSlot(bool)
    def print_image(self, dat):
        self.pixmap = QPixmap(OPERATE_MAP_FILE)
        self.map_image.setPixmap(self.pixmap)

    def change_index_show_status(self):
        self.index_show_status = not self.index_show_status
        map_data = self.operate_map.formatted_address(self.address, postal_code=self.index_show_status)
        self.full_address_line.setText(map_data)
        self.update_picture()
        print(self.index_show_status)

    def line_request(self):
        self.status_label.setText("request address")

        self.address = self.request_line.text()
        print(f"address:{self.address}")
        if self.address != "":
            map_data = self.operate_map.find_adress(self.address, postal_code=self.index_show_status)
            if map_data is not ADDRESS_NOT_FOUND:
                self.update_picture()
                print(map_data)
                self.full_address_line.setText(map_data)
            else:
                self.status_label.setText("error in address request")
        else:
            self.status_label.setText("request line is void")

    def dump_request(self):
        self.request_line.setText("")
        self.full_address_line.setText("")
        self.operate_map.delete_pt()
        self.update_picture()

    def radio_button_clicked(self):
        self.operate_map.change_l(self.sender().text())

    def update_picture(self):
        print("updating picture")
        self.status_label.setText("updating picture")

        self.map_image.setPixmap(QPixmap("Wait_img.jpg"))
        with open(OPERATE_MAP_FILE, "wb") as file:
            file.write(self.operate_map.get_picture())
        self.pixmap = QPixmap(OPERATE_MAP_FILE)
        self.map_image.setPixmap(self.pixmap)

        self.status_label.setText("picture is draw")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_PageUp:
            self.operate_map.change_zoom("zoom_in")
            self.update_picture()
        elif event.key() == Qt.Key_PageDown:
            self.operate_map.change_zoom("zoom_away")
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

    def closeEvent(self, event):
        os.remove(OPERATE_MAP_FILE)


    def mouseReleaseEvent(self, event):
        if not 700 > event.x() > 100 and not 550 > event.y() > 100:
            return
        x, y = self.operate_map.screen_to_geo((event.x() - 100, event.y() - 100))
        self.operate_map.pt = [x, y]
        if event.button() == Qt.LeftButton:
            self.full_address_line.setText(self.operate_map.formatted_address(f"{x},{y}", postal_code=self.index_show_status))
            self.update_picture()
        elif event.button() == Qt.RightButton:
            # print(f'x:{x}, y:{y}, {x},{y}')
            # print('jjjjj', find_business('Аптека', f'{x},{y}', '0.00045045045,0.00045045045'))
            # self.full_address_line.setText(find_business('Аптека', f'{x},{y}', '1,1')['geometry']['coordinates']['properties']['CompanyMetaData']['name'])
            try:
                org = find_business('', f'{x},{y}', '0.00045045045,0.00045045045')['properties']['CompanyMetaData']['name']
            except TypeError:
                org = None
            self.full_address_line.setText(org if org else 'Организация не найдена')
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