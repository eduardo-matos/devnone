import os


DEBUG = False
REDIS_DB = 1
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite://')
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:8000/')

try:
    from devnone.conf_local import *
except:
    pass
