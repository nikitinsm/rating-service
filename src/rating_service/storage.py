# -*- coding: utf-8 -*-
import os
import redis


class MemoryStorage(object):

    key_value_storage = {}

    def get(self, key):
        return self.key_value_storage.get(key) or None

    def set(self, key, value):
        self.key_value_storage[key] = value

    def increment(self, key, value):
        self.key_value_storage.setdefault(key, 0)
        self.key_value_storage[key] += value

    def decrement(self, key, value):
        self.key_value_storage.setdefault(key, 0)
        self.key_value_storage[key] -= value

    def delete(self, key):
        self.key_value_storage.pop(key)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class RedisStorage(object):

    pipeline = None
    connection = redis.ConnectionPool\
        ( host=os.environ.get('REDIS_PORT_6379_TCP_ADDR')
        , port=6379
        , db=0
        )
    redis = redis.Redis\
        ( connection_pool=connection
        )

    def get_redis(self):
        return self.pipeline or self.redis

    def get(self, key):
        return self.get_redis().get(key)

    def set(self, key, value):
        self.get_redis().set(key, value)

    def increment(self, key, value):
        self.get_redis().incr(key, value)

    def decrement(self, key, value):
        self.get_redis().decr(key, value)

    def delete(self, key):
        self.get_redis().delete(key)

    def __enter__(self):
        self.pipeline = self.redis.pipeline()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pipeline and self.pipeline.execute()


Storage = RedisStorage