import requests, sys, os, io


class Map:
    def __init__(self, ll, spn, l):
        self.ll = ll
        self.spn = spn
        self.l = l
        self.api_server = "http://static-maps.yandex.ru/1.x/"
        self.pt = None

    def get_picture(self):
        map_params = {
            "ll": self.ll,
            "spn": self.spn,
            "l": self.l,
            "pt": self.pt
            }
        response = requests.get(self.api_server, params=map_params)
        img = io.BytesIO(response.content)
        return img

    def make_pt(self, pt_ll):
        self.pt = pt_ll

