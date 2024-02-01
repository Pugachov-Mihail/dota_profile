import requests


async def get_matches(id: int):
    data = requests.get(f'http://127.0.0.2:8001/get-matches/{id}')
    return data.json()