import redis
from devnone.app import app


def create_redis():
    redis_ = redis.StrictRedis(db=app.config['REDIS_DB'])
    redis_.flushdb()

    return redis_


def drop_redis(redis_):
    redis_.flushdb()
