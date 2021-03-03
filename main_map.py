from geocoder import *
import math


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
        self.api_server = API_SERVER
        self.pt = None

    def map_settings(self, ll, zoom, l):
        self.ll = [ll[1], ll[0]]
        self.zoom = zoom
        self.l = l

    def screen_to_geo(self, pos):
        dy = 225 - pos[1]
        dx = pos[0] - 300
        lon = self.ll[0]
        lat = self.ll[1]
        zoom = self.zoom
        lx = lon + dx * COORD_TO_GEO_X * math.pow(2, MAX_ZOOM - zoom)
        ly = lat + dy * COORD_TO_GEO_Y * math.cos(math.radians(lat)) * math.pow(2, MAX_ZOOM - zoom)
        return lx, ly

    def get_picture(self):
        print(f"ll: {self.ll}; pt: {self.pt}", self.zoom)
        map_params = {
            'll': f"{self.ll[0]},{self.ll[1]}",
            'l': self.l,
            'z': self.zoom,
            'pt': f"{self.pt[0]},{self.pt[1]}" if self.pt is not None else None
        }
        response = requests.get(self.api_server, params=map_params)
        return response.content

    def make_pt(self, pt_ll):
        self.pt = pt_ll

    def move(self, direct):
        if direct == 'left':
            if MIN_MOVE_X < self.screen_to_geo((0, IMAGE_SIZE[1] / 2))[0] < MAX_MOVE_X:
                new_ll = self.screen_to_geo((0, IMAGE_SIZE[1] / 2))
        elif direct == 'right':
            if MIN_MOVE_X < self.screen_to_geo((IMAGE_SIZE[0], IMAGE_SIZE[1] / 2))[0] < MAX_MOVE_X:
                new_ll = self.screen_to_geo((IMAGE_SIZE[0], IMAGE_SIZE[1] / 2))
        elif direct == 'down':
            if MIN_MOVE_Y < self.screen_to_geo((IMAGE_SIZE[0] / 2, IMAGE_SIZE[1]))[1] < MAX_MOVE_Y:
                new_ll = self.screen_to_geo((IMAGE_SIZE[0] / 2, IMAGE_SIZE[1]))
        elif direct == 'up':
            if MIN_MOVE_Y < self.screen_to_geo((IMAGE_SIZE[0] / 2, 0))[1] < MAX_MOVE_Y:
                new_ll = self.screen_to_geo((IMAGE_SIZE[0] / 2, 0))
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

