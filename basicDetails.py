OPERATE_MAP_FILE = "__map__.png"

START_ZOOM = 15
START_ADDRESS = "проспект Свободный 74г"
START_VISION = "map"
ADDRESS_NOT_FOUND = "nf"
IMAGE_SIZE = [600, 450]
IMAGE_POS = [100, 100]


MAX_MOVE_Y = 85
MIN_MOVE_Y = -MAX_MOVE_Y
MAX_MOVE_X = 175
MIN_MOVE_X = -MAX_MOVE_X

ZOOM_STEP = 1
MAX_ZOOM = 15
MIN_ZOOM = 3

LAT_STEP = 0.008  # Шаги при движении карты по широте и долготе
LON_STEP = 0.02

# Пропорции пиксельных и географических координат.
COORD_TO_GEO_X = 0.0000428
COORD_TO_GEO_Y = 0.0000428

API_SERVER = "http://static-maps.yandex.ru/1.x/"

MAPS_VIEW = {
    "Спутник": "sat",
    "Карта": "map",
    "Гибрид": "sat,skl"
}