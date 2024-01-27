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
from src.log import logger

class MyRedis():
    def __init__(self):
        self.host = CONFIG['REDIS_HOST']
        self.port = CONFIG['REDIS_PORT']
        self.password = CONFIG['REDIS_PASSWORD']
        try:
            self.r = redis.Redis(host=self.host, port=self.port, password=self.password)
            self.r.ping()
            logger.info(f'连接redis成功')
        except Exception as e:
            logger.error(f'连接redis失败 {e}')


    def set_redis(self, key, value, ex=60 * 5):
        """
        设置值
        :param key:
        :param value:
        :param ex: 过期时间（秒）
        :return:
        """
        self.r.set(key, value, ex)
        logger.info(f'设置redis成功 {key} {value}')

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
    def get_redis(self, key):
        """
        获取值
        :param key:
        :return:
        """
        ret_=self.r.get(key)
        if ret_:
            return ret_.decode('utf-8')
        else:
            return None

share_redis = MyRedis()