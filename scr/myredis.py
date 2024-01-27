# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : myredis.py
# @Time : 2024/1/26 11:07
# -------------------------------
# REDIS操作类

import redis
from config import CONFIG


class MyRedis():
    def __init__(self):
        self.host = CONFIG['REDIS_HOST']
        self.port = CONFIG['REDIS_PORT']
        self.password = CONFIG['REDIS_PASSWORD']
        self.db = 0
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, password=self.password, db=self.db)
        self.r = redis.Redis(connection_pool=self.pool)

    def set_redis(self, key, value, ex=60 * 5):
        """
        设置值
        :param key:
        :param value:
        :param ex: 过期时间（秒）
        :return:
        """
        self.r.set(key, value, ex)

    def update_redis(self, key, value, ex=60 * 5):
        """
        更新值
        :param key:
        :param value:
        :return:
        """
        self.r.set(key, value, ex)

    def del_redis(self, key):
        """
        删除值
        :param key:
        :return:
        """
        self.r.delete(key)
