import requests, sys, os, io
from geocoder import *

MAPS_VIEW = {
    "Спутник": "sat",
    "Карта": "map",
    "Гибрид": "sat,skl"
}

ADDRESS_NOT_FOUND = False


class Map:
    def __init__(self, ll, zom, l):
        # self.ll = [ll[1], ll[0]]
        self.ll =[0, 0]
        self.zom = zom
        self.l = l
        self.api_server = "http://static-maps.yandex.ru/1.x/"
        self.pt = None

    def get_picture(self):
        # map_params = {
        #     "ll": self.ll,
        #     "zom": f"{self.zom},{self.zom}",
        #     "l": self.l,
        #     # "pt": self.pt
        #     }
        # print(self.ll, self.zom, self.l)
        print("request picture")
        print(f"ll: {self.ll}; pt: {self.pt}", self.zom)
        map_params = {
            'll': f"{self.ll[0]},{self.ll[1]}",
            'l': self.l,
            'z': self.zom,
            'pt': f"{self.pt[0]},{self.pt[1]}" if self.pt is not None else None
        }
        # response = requests.get("http://static-maps.yandex.ru/1.x/?ll=37.530887,55.703118&zom=0.002,0.002&l=map")
        response = requests.get(self.api_server, params=map_params)
        return response.content

    def make_pt(self, pt_ll):
        self.pt = pt_ll

    def move(self, direct):
        # print("move card")
        if direct == 'left':
            self.ll[0] -= 10 / self.zom
        elif direct == 'right':
            self.ll[0] += 10 / self.zom
        elif direct == 'up':
            self.ll[1] += 10 / self.zom
        elif direct == 'down':
            self.ll[1] -= 10 / self.zom

        # print("move is end")

    def zoom(self, direct):
        if direct == 'zoom_in':
            self.zom += 1
        elif direct == 'zoom_away':
            self.zom -= 1

    def change_l(self, new_l):
        self.l = MAPS_VIEW[new_l]

    def find_adress(self, adress, postal_code=False, century_map=True):
        print("search address")

        new_ll = [*get_coordinates(adress)]
        if new_ll[0] is None:
            return ADDRESS_NOT_FOUND
        if century_map:
            self.ll = new_ll[:]
        self.pt = new_ll[:]
        if not geocode(adress):
            return
        # print(geocode(adress))
        output = geocode(adress)['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
        if postal_code:
            try:
                output += ' ' + geocode(adress)['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
            except KeyError:
                pass
        print(f"new ll: {new_ll}")
        print(output)
        return output

    def delete_pt(self):
        self.pt = None

