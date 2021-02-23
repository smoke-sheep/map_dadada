from basicDetails import *

from PyQt5 import QtCore
from main_map import Map, ADDRESS_NOT_FOUND


class mapStream(QtCore.QObject):
    newImage = QtCore.pyqtSignal(bool)
    newAddress = QtCore.pyqtSignal(str)
    mapError = QtCore.pyqtSignal(str)

    def __init__(self):
        super(mapStream, self).__init__()
        self.map = Map([37.530887, 55.703118], 0.02, "map")

    def get_address(self, search_request, postal_code=False):
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
            self.mapError.emit(f"get picture error: {e}")

    def run(self):
        while True:
            pass