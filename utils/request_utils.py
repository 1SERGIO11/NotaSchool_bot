import requests
from requests import Response

from venv import API_BASE_URL

base_url = API_BASE_URL

def get_request(url: str, json: dict[str, any] = {}) -> Response:
    return requests.get(
        url=f"{base_url}{url}",
        json=json,
    )


def post_request(url: str, json: dict[str, any] = {}) -> Response:
    return requests.post(
        url=f"{base_url}{url}",
        json=json,
    )