import requests, sys, os, io
from geocoder import *
import math
MAPS_VIEW = {
    "Спутник": "sat",
    "Карта": "map",
    "Гибрид": "sat,skl"
}

ADDRESS_NOT_FOUND = "nf"
IMAGE_SIZE = [600, 450]
IMAGE_POS = [100, 100]


ZOOM_STEP = 1
MAX_MOVE = 85
MIN_MOVE = -85
MAX_ZOOM = 15
MIN_ZOOM = 3


def formatted_address(adress, postal_code=False):
    output = geocode(adress)['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
    if postal_code:
        try:
            output += " " + geocode(adress)['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
        except:
            print("нет индекса")

    print("formatted_address", adress, output)
    return output


class Map:
    def __init__(self):
        self.ll = [0, 0]
        self.zoom = 1
        self.l = "map"
        self.api_server = "http://static-maps.yandex.ru/1.x/"
        self.pt = None

    def map_settings(self, ll, zoom, l):
        self.ll = [ll[1], ll[0]]
        self.zoom = zoom
        self.l = l

    def screen_to_geo(self, pos):
        LAT_STEP = 0.008  # Шаги при движении карты по широте и долготе
        LON_STEP = 0.02
        coord_to_geo_x = 0.0000428  # Пропорции пиксельных и географических координат.
        coord_to_geo_y = 0.0000428
        dy = 225 - pos[1]
        dx = pos[0] - 300
        lon = self.ll[0]
        lat = self.ll[1]
        zoom = self.zoom
        lx = lon + dx * coord_to_geo_x * math.pow(2, 15 - zoom)
        ly = lat + dy * coord_to_geo_y * math.cos(math.radians(lat)) * math.pow(2, 15 - zoom)
        return lx, ly

    def get_picture(self):
        # map_params = {
        #     "ll": self.ll,
        #     "spn": f"{self.spn},{self.spn}",
        #     "l": self.l,
        #     # "pt": self.pt
        #     }
        # print(self.ll, self.spn, self.l)
        # print("request picture")
        print(f"ll: {self.ll}; pt: {self.pt}", self.zoom)
        map_params = {
            'll': f"{self.ll[0]},{self.ll[1]}",
            'l': self.l,
            'z': self.zoom,
            'pt': f"{self.pt[0]},{self.pt[1]}" if self.pt is not None else None
        }
        # response = requests.get("http://static-maps.yandex.ru/1.x/?ll=37.530887,55.703118&spn=0.002,0.002&l=map")
        response = requests.get(self.api_server, params=map_params)
        return response.content

    def make_pt(self, pt_ll):
        self.pt = pt_ll

    def move(self, direct):
        # self.screen_to_geo(IMAGE_SIZE[0] / 2 + IMAGE_POS[0], IMAGE_SIZE[1] / 2 + IMAGE_POS[1])
        # print("move card")
        if direct == 'left':
            if MIN_MOVE < self.screen_to_geo((0, IMAGE_SIZE[1] / 2))[0] < MAX_MOVE:
                new_ll = self.screen_to_geo((0, IMAGE_SIZE[1] / 2))
            # self.ll[0] -= k
        elif direct == 'right':
            if MIN_MOVE < self.screen_to_geo((IMAGE_SIZE[0], IMAGE_SIZE[1] / 2))[0] < MAX_MOVE:
                new_ll = self.screen_to_geo((IMAGE_SIZE[0], IMAGE_SIZE[1] / 2))
            # self.ll[0] += k
        elif direct == 'down':
            if MIN_MOVE < self.screen_to_geo((IMAGE_SIZE[0] / 2, IMAGE_SIZE[1]))[1] < MAX_MOVE:
                new_ll = self.screen_to_geo((IMAGE_SIZE[0] / 2, IMAGE_SIZE[1]))
            # self.ll[1] += k
        elif direct == 'up':
            if MIN_MOVE < self.screen_to_geo((IMAGE_SIZE[0] / 2, 0))[1] < MAX_MOVE:
                new_ll = self.screen_to_geo((IMAGE_SIZE[0] / 2, 0))
            # self.ll[1] -= k
        try:
            self.ll = new_ll[:]
        except Exception:
            print('максимальная или минимальная координата достигнута')

    def change_zoom(self, direct):
        if direct == 'zoom_in':
            self.zoom += ZOOM_STEP
        elif direct == 'zoom_away':
            self.zoom -= ZOOM_STEP

        if self.zoom > MAX_ZOOM:
            self.zoom = MAX_ZOOM
            return "zoom level is maximum"
        if self.zoom < MIN_ZOOM:
            self.zoom = MIN_ZOOM
            return "zoom level is minimum"

        return "zoom"

    def change_l(self, new_l):
        self.l = MAPS_VIEW[new_l]

    def find_adress(self, adress, postal_code=False):
        print("search address")

        new_ll = [*get_coordinates(adress)]
        if new_ll[0] is None:
            return ADDRESS_NOT_FOUND
        self.ll = new_ll[:]
        print('new_ll', new_ll)
        self.pt = new_ll[:]
        data = formatted_address(adress, postal_code=postal_code)
        print("find adress", data)
        return data

    def delete_pt(self):
        self.pt = None

