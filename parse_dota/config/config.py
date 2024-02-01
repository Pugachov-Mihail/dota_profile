import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

DOTA_API = os.environ.get("DOTA_API")

MONGO_USER = os.environ.get("MONGO_USERNAME")
MONGO_PASS = os.environ.get("MONGO_PASSWORD")

CONNECT = f"mongodb://{MONGO_USER}:{MONGO_PASS}@mongo:27017/"

client = MongoClient(CONNECT)

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
