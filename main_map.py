import requests, sys, os, io


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
        print(self.ll, self.spn, self.l)
        map_params = {
            'll': f"{self.ll[0]},{self.ll[1]}",
            'l': self.l,
            'spn': f"{self.spn},{self.spn}",
            'pt': self.pt
        }

        response = requests.get(self.api_server, params=map_params)
        return response.content

    def make_pt(self, pt_ll):
        self.pt = pt_ll

    def move(self, direct):
        try:
            print(direct)
            if direct == 'left':
                self.ll[0] -= 0.1 * self.spn
            elif direct == 'right':
                self.ll[0] += 0.1 * self.spn
            elif direct == 'up':
                self.ll[1] += 0.1 * self.spn
            elif direct == 'down':
                self.ll[1] -= 0.1 * self.spn
        except Exception as e:
            print(e)

    def zoom(self, direct):
        if direct == 'zoom_in':
            self.spn *= 0.1
        elif direct == 'zoom_away':
            self.spn /= 0.1

    def change_l(self, new_l):
        self.l = new_l