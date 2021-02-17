import sys
import requests


def geocode(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        raise RuntimeError(f'Ошибка выполнения запроса:\n' \
                           f'{response.url}\n' \
                           f'Статус: {response.status_code} {response.reason}')
    data = response.json()
    features = data["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"] if features else None


def get_coordinates(address):
    toponym = geocode(address)
    if toponym is None:
        return None, None
    toponym_coordinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coordinates.split(" ")
    return float(toponym_longitude), float(toponym_lattitude)


def get_ll_span(address):
    toponym = geocode(address)
    if toponym is None:
        return None, None
    toponym_coordinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coordinates.split(" ")
    ll = ','.join([toponym_longitude, toponym_lattitude])

    envelope = toponym['boundedBy']['Envelope']
    left, bottom = map(float, envelope['lowerCorner'].split(' '))
    right, top = map(float, envelope['upperCorner'].split(' '))

    dx = abs(left - right) / 2
    dy = abs(bottom - top) / 2

    span = f'{dx},{dy}'

    return ll, span
