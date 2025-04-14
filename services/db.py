from pymongo import MongoClient

from . import MONGO_DB_NAME, MONGO_URI

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
