import logging.config
import os

import dotenv
import yaml


dotenv.load_dotenv(dotenv_path=os.environ.get("CONFIG", None))

APP_NAME = "ai-food-ingredient"
ENV = os.getenv("ENV")

PORT = int(os.environ['PORT']) if os.getenv('PORT', None) else None

LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']

MONGO_DB_CLOUD_HOST = os.environ['MONGO_DB_CLOUD_HOST']
MONGO_DB_DATABASE = os.environ['MONGO_DB_DATABASE']
MONGO_DB_USER = os.environ['MONGO_DB_USER']
MONGO_DB_PASSWORD = os.environ['MONGO_DB_PASSWORD']

if ENV is not None:
    LOG_CONFIG = "logging.yml"
    DEBUG = False
    FLASK_USE_RELOADER = False
else:
    LOG_CONFIG = "logging_local.yml"
    DEBUG = True
    FLASK_USE_RELOADER = True


with open(LOG_CONFIG, 'r') as fout:
    logging.config.dictConfig(yaml.load(fout, Loader=yaml.FullLoader))
