from basicDetails import *

from PyQt5 import QtCore
from main_map import Map, ADDRESS_NOT_FOUND


class mapStream(QtCore.QObject, Map):
    newImage = QtCore.pyqtSignal(bool)
    newAddress = QtCore.pyqtSignal(str)
    mapError = QtCore.pyqtSignal(str)
    mapData = QtCore.pyqtSignal(str)

    def __init__(self, ll, zoom, l):
        super(mapStream, self).__init__()
        self.map_settings(ll, zoom, l)

    def change_l(self, new_l):
        super(mapStream, self).change_l(new_l)
        self.draw_picture()

    def change_zoom(self, direct):
        super(mapStream, self).change_zoom(direct)
        self.draw_picture()

    def find_adress(self, adress, postal_code=False):
        data = super(mapStream, self).find_adress(adress, postal_code=postal_code)
        print(f"finded address {data}")
        self.newAddress.emit(data)
        if data != ADDRESS_NOT_FOUND:
            self.draw_picture()

    def move(self, direct):
        self.newAddress.emit(super(mapStream, self).move(direct))
        self.draw_picture()

    def formatted_address(self, adress, postal_code=False):
        super(mapStream, self).formatted_address(adress, postal_code=postal_code)

    def draw_picture(self):
        try:
            with open(OPERATE_MAP_FILE, "wb") as file:
                file.write(self.get_picture())

            self.newImage.emit(True)
        except Exception as e:
            self.mapError.emit(f"get picture error: {e}")

    """def get_address(self, search_request, postal_code=False):
        data = self.map.find_adress(search_request, postal_code=postal_code)

        if data is not ADDRESS_NOT_FOUND:
            self.newAddress.emit(data)
        else:
            self.mapError.emit("error in address request")

        try:
            with open(OPERATE_MAP_FILE, "wb") as file:
                file.write(self.map.get_picture())

            self.newImage.emit(True)
        except Exception as e:
            self.mapError.emit(f"get picture error: {e}")"""

    def run(self):
        while True:
            pass