import os

import dotenv

dotenv.load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv("db_url")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle': 60}
SECRET_KEY = os.getenv("secret_key")
DEBUG = True
