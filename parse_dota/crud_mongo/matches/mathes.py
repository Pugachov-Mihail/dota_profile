import logging

from config import config
from pymongo import ASCENDING, errors
from fastapi import HTTPException


async def find_matches_player(player: int, id: int):
    player = config.client["Matches"][f"{player}"].find_one({'match_id': id})
    return player


async def write_matches_user(data):
    try:
        matches = config.client["Matches"]
        matches[f'{id}'].create_index([("match_id", ASCENDING)], unique=True)
        matches[f'{id}'].insert_many(data)
        return True
    except errors.BulkWriteError:
        logging.warn("Такие матчи уже записаны")
        return False


