from dotenv import load_dotenv
from os import environ, path

import dotenv
from dotenv.main import find_dotenv

dotenvfile = find_dotenv()
load_dotenv(dotenvfile)


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = dotenv.get_key(dotenvfile, "SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = dotenv.get_key(dotenvfile, "SQLALCHEMY_DATABASE_URI")
    # SESSION_COOKIE_SECURE = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    pass

class DevConfig(Config):
    
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = dotenv.get_key(dotenvfile, "SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


class TestingConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    DB_Employee = "admin"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = False