import requests, sys, os, io
from geocoder import *
import math
MAPS_VIEW = {
    "Спутник": "sat",
    "Карта": "map",
    "Гибрид": "sat,skl"
}

ADDRESS_NOT_FOUND = False
IMAGE_SIZE = [600, 450]
IMAGE_POS = [100, 100]

class Map:
    def __init__(self, ll, zoom, l):
        self.ll = [ll[1], ll[0]]
        self.zoom = zoom
        self.l = l
        self.api_server = "http://static-maps.yandex.ru/1.x/"
        self.pt = None

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
        k = 1 / (self.zoom * 3)
        # print("move card")
        if direct == 'left':
            new_ll = self.screen_to_geo((0, IMAGE_SIZE[1] / 2))
            # self.ll[0] -= k
        elif direct == 'right':
            new_ll = self.screen_to_geo((IMAGE_SIZE[0], IMAGE_SIZE[1] / 2))
            # self.ll[0] += k
        elif direct == 'down':
            new_ll = self.screen_to_geo((IMAGE_SIZE[0] / 2, IMAGE_SIZE[1]))
            # self.ll[1] += k
        elif direct == 'up':
            new_ll = self.screen_to_geo((IMAGE_SIZE[0] / 2, 0))
            # self.ll[1] -= k
        self.ll = new_ll[:]
        # print(f'new_ll:{new_ll}')

        # print("move is end")

    def change_zoom(self, direct):
        if direct == 'zoom_in':
            self.zoom += 1
        elif direct == 'zoom_away':
            self.zoom -= 1

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
        return self.formatted_address(adress, postal_code=postal_code)

    def formatted_address(self, adress, postal_code=False):
        output = geocode(adress)['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
        if postal_code:
            output += geocode(adress)['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
        # print(f"new ll: {new_ll}")
        # print(adress, output)
        return output

    def delete_pt(self):
        self.pt = None

