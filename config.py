from dotenv import load_dotenv
from os import environ, path

import dotenv
from dotenv.main import find_dotenv

dotenvfile = find_dotenv()
load_dotenv(dotenvfile)

# Basic config object this is the default parameters
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = dotenv.get_key(dotenvfile, "SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = dotenv.get_key(dotenvfile, "SQLALCHEMY_DATABASE_URI")
    # SESSION_COOKIE_SECURE = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Pass values from default config
class ProductionConfig(Config):
    pass

# Developer option config, uses test.db
class DevConfig(Config):
    
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = dotenv.get_key(dotenvfile, "SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'