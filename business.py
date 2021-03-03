import sys
from io import BytesIO
import requests
from pprint import pprint


def find_businesses(place, ll, spn, locale='ru_RU'):
    search_api_server = "https://search-maps.yandex.ru/v1/"

    search_params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": place,
        "lang": locale,
        "ll": ll,
        'spn': spn,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)

    if not response:
        raise RuntimeError(f'Ошибка выполнения запроса:\n' \
                           f'{response.url}\n' \
                           f'Статус: {response.status_code} {response.reason}')
    data = response.json()
    features = data["features"]
    return features


def find_business(place, ll, spn, locale='ru_RU'):
    orgs = find_businesses(place, ll, spn, locale)
    print("busines: ", end="")
    if orgs:
        pprint(orgs[0])
        return orgs[0]
