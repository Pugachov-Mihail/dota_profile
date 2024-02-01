import logging

import requests
from fastapi import FastAPI, HTTPException
from config import config
from crud_mongo.matches import mathes

app = FastAPI()


@app.get('/get-matches/{id}')
async def get_matches(id: int):
    data = requests.get(f'{config.DOTA_API}/players/{id}/matches').json()
    if len(data) > 0:
        result = await mathes.write_matches_user(data)
        if result:
            return {"message": "Матчи записаны"}
        return HTTPException(
            status_code=400,
            detail="Такие матчи уже записаны"
        )
    else:
        return HTTPException(
             status_code=400,
             detail="Нет доступных матчей"
        )

