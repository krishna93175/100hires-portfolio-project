import requests

from core.config import API_KEY


BASE_URL = "https://www.googleapis.com/youtube/v3"


def youtube_get(endpoint, params):

    params["key"] = API_KEY

    response = requests.get(f"{BASE_URL}/{endpoint}", params=params)

    response.raise_for_status()

    return response.json()