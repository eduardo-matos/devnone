DEBUG = False
REDIS_DB = 1

try:
    from devnone.conf_local import *
except:
    pass
