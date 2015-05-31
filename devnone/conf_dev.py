DEBUG = True
REDIS_DB = 2

try:
    from devnone.conf_local import *
except:
    pass
