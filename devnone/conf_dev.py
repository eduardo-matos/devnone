DEBUG = True
REDIS_DB = 2
SQLALCHEMY_DATABASE_URI = 'sqlite://'
BASE_URL = 'http://localhost:8000'

try:
    from devnone.conf_local import *
except:
    pass
