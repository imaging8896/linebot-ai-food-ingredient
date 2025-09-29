import logging

import app_config

from food.db.mongo_db import MongoDB

mongo_db = MongoDB(
    MongoDB.Parameter(
        host=app_config.MONGO_DB_CLOUD_HOST,
        user=app_config.MONGO_DB_USER,
        password=app_config.MONGO_DB_PASSWORD,
        database=app_config.MONGO_DB_DATABASE,
    )
)

app_logger = logging.getLogger("app")
