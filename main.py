from basicDetails import *
from main_map import ADDRESS_NOT_FOUND, formatted_address
from mapStream import mapStream
from business import *
from geocoder import *

from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import Qt

import sys
import os

INDEX_NOT_SHOW = False
INDEX_SHOW = True


class MapWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.address = START_ADDRESS
        self.organisation_type = "Продукты"
        uic.loadUi("design.ui", self)
        self.initUi()

    def initUi(self):
        self.map_image.setPixmap(QPixmap("Wait_img.jpg"))

        for i in range(0, 3):
            getattr(self, f"radioButton_{i}").clicked.connect(self.radio_button_clicked)
        self.radioButton_0.setChecked(True)
        self.setFocusPolicy(Qt.WheelFocus)

        for i in range(3, 13):
            getattr(self, f"radioButton_{i}").clicked.connect(self.choice_organisation_type)
        self.radioButton_3.setChecked(True)

        self.request_button.clicked.connect(self.line_request)
        self.dump_button.clicked.connect(self.dump_request)

        self.index_show_status = INDEX_NOT_SHOW
        self.index_checkBox.stateChanged.connect(self.change_index_show_status)

        self.thread = QtCore.QThread()  # создаем поток
        self.operate_map = mapStream(get_coordinates(START_ADDRESS), START_ZOOM, START_VISION)
        self.operate_map.moveToThread(self.thread)
        self.operate_map.newImage.connect(self.print_image)  # подключаем события
        self.operate_map.newAddress.connect(self.print_address)
        self.operate_map.mapError.connect(self.map_error)
        self.thread.started.connect(self.operate_map.run)
        self.thread.start()  # запустим поток

    @QtCore.pyqtSlot(str)
    def map_error(self, data):
        print(data)

    @QtCore.pyqtSlot(str)
    def print_address(self, data):
        print(data)
        if data != ADDRESS_NOT_FOUND:
            self.full_address_line.setText(data)
        else:
            self.full_address_line.setText("address not found")

    @QtCore.pyqtSlot(bool)
    def print_image(self, data):
        print("printing image")
        self.pixmap = QPixmap(OPERATE_MAP_FILE)
        self.map_image.setPixmap(self.pixmap)

        self.status_label.setText("picture is draw")

    def choice_organisation_type(self):
        self.organisation_type = self.sender().text()

    def change_index_show_status(self):
        self.index_show_status = not self.index_show_status
        if self.address != "":
            self.full_address_line.setText(formatted_address(self.address, postal_code=self.index_show_status))
        else:
            self.status_label.setText("request line is void")
        print(self.index_show_status)

    def line_request(self):
        self.status_label.setText("request address")

        self.address = self.request_line.text()
        print(f"address:{self.address}")
        if self.address != "":
            self.operate_map.find_adress(self.address, postal_code=self.index_show_status)
        else:
            self.status_label.setText("request line is void")

    def dump_request(self):
        self.request_line.setText("")
        self.full_address_line.setText("")
        self.address = START_ADDRESS
        self.operate_map.find_adress(START_ADDRESS)

    def radio_button_clicked(self):
        self.operate_map.change_l(self.sender().text())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_PageUp:
            self.operate_map.change_zoom("zoom_in")
        elif event.key() == Qt.Key_PageDown:
            self.operate_map.change_zoom("zoom_away")
        elif event.key() == Qt.Key_Down:
            self.operate_map.move("down")
        elif event.key() == Qt.Key_Up:
            self.operate_map.move("up")
        elif event.key() == Qt.Key_Left:
            self.operate_map.move("left")
        elif event.key() == Qt.Key_Right:
            self.operate_map.move("right")
        else:
            print(event.key())

    def closeEvent(self, event):
        os.remove(OPERATE_MAP_FILE)

    def mouseReleaseEvent(self, event):
        print(f"mouse event: {event.x()},{event.y()}")
        if not(700 > event.x() > 100) or not(550 > event.y() > 100):
            return

        self.request_line.setText("")
        self.full_address_line.setText("")

        x, y = self.operate_map.screen_to_geo((event.x() - 100, event.y() - 100))
        self.operate_map.pt = [x, y]
        if event.button() == Qt.LeftButton:
            self.address = formatted_address(f"{x},{y}", postal_code=self.index_show_status)
            self.full_address_line.setText(self.address)
        elif event.button() == Qt.RightButton:
            try:
                print("поиск организации")
                org = find_business(self.organisation_type, f'{x},{y}', '0.00045045045,0.00045045045')['properties']['CompanyMetaData']['name']
                print(org)
            except TypeError:
                org = None
            self.full_address_line.setText(org if org else 'Организация не найдена')

        self.operate_map.draw_picture()
        self.print_image(False)


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