from dataclasses import dataclass

from pymongo import MongoClient

from .logger import logger
from .user import get_user
from ..helper.decorator import log_call


class MongoDB:

    @dataclass(frozen=True, kw_only=True, slots=True)
    class Parameter:
        host: str
        user: str
        password: str
        database: str
    

    def __init__(self, parameter: Parameter):
        logger.debug(f"Mongo DB {parameter.host} connecting")
        self.client = MongoClient(f"mongodb+srv://{parameter.user}:{parameter.password}@{parameter.host}", socketTimeoutMS=300000, serverSelectionTimeoutMS=30000, connect=True, maxPoolSize=20)
        self.mongo_db = self.client[parameter.database]

    # User collection

    @log_call(logger)
    def get_user(self, user_id: str):
        return get_user(self.mongo_db, user_id)

    # User collection end
