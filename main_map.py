import requests, sys, os, io
from geocoder import *

MAPS_VIEW = {
    "Спутник": "sat",
    "Карта": "map",
    "Гибрид": "sat,skl"
}


class Map:
    def __init__(self, ll, spn, l):
        self.ll = [ll[1], ll[0]]
        self.spn = spn
        self.l = l
        self.api_server = "http://static-maps.yandex.ru/1.x/"
        self.pt = None

    def get_picture(self):
        # map_params = {
        #     "ll": self.ll,
        #     "spn": f"{self.spn},{self.spn}",
        #     "l": self.l,
        #     # "pt": self.pt
        #     }
        # print(self.ll, self.spn, self.l)
        print("request picture")
        print(f"ll: {self.ll}; pt: {self.pt}")
        map_params = {
            'll': f"{self.ll[0]},{self.ll[1]}",
            'l': self.l,
            'spn': f"{self.spn},{self.spn}",
            'pt': f"{self.pt[0]},{self.pt[1]}"
        }
        # response = requests.get("http://static-maps.yandex.ru/1.x/?ll=37.530887,55.703118&spn=0.002,0.002&l=map")
        response = requests.get(self.api_server, params=map_params)
        return response.content

    def make_pt(self, pt_ll):
        self.pt = pt_ll

    def move(self, direct):
        # print("move card")
        if direct == 'left':
            self.ll[0] -= 0.1 * self.spn
        elif direct == 'right':
            self.ll[0] += 0.1 * self.spn
        elif direct == 'up':
            self.ll[1] += 0.1 * self.spn
        elif direct == 'down':
            self.ll[1] -= 0.1 * self.spn

        # print("move is end")

    def zoom(self, direct):
        if direct == 'zoom_in':
            self.spn /= 0.1
        elif direct == 'zoom_away':
            self.spn *= 0.1

    def change_l(self, new_l):
        self.l = MAPS_VIEW[new_l]

    def find_adress(self, adress, postal_code=False):
        print("search address")

        new_ll = [*get_coordinates(adress)]
        self.ll = new_ll
        self.pt = new_ll
        output = geocode(adress)['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
        if postal_code:
            output += geocode(adress)['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
        print(f"new ll: {new_ll}")
        print(output)
        return output

    def delete_pt(self):
        self.pt = None

