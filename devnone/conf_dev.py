DEBUG = True
REDIS_DB = 2
SQLALCHEMY_DATABASE_URI = 'sqlite://'

try:
    from devnone.conf_local import *
except:
    pass
