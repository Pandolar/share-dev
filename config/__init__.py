# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : __init__.py.py
# @Time : 2024/1/18 15:32
# -------------------------------
CONFIG = {
    # 用户和数据库配置
    "USER": "admin",
    "PASSWORD": "foxfox",
    "PORT": 18980,  # 服务端口号
    "DB_HOST": "127.0.0.1",
    "DB_USER": "share_dev",
    "DB_PASSWORD": "share_dev",
    "DB_NAME": "share_dev",
    "DB_PORT": 33062,
    # redis配置
    "REDIS_HOST": "127.0.0.1",
    "REDIS_PORT": 6379,
    "REDIS_PASSWORD": "",
    # share的配置
    "SHARE_HOST": "go.foxaigc.com",  # share主地址 必须开HTTPS
    "SHARE_KEY": "fba2mjbfi2asf3d",  # share的api key
    "MAX_USER_IN_CAR": 5,  # 车内最大人数

    # 独角数据库的配置
    "DUJIAO_DB_HOST": "127.0.0.1",
    "DUJIAO_DB_USER": "dujiao",
    "DUJIAO_DB_PASSWORD": "dujiao",
    "DUJIAO_DB_NAME": "dujiao",
    "DUJIAO_DB_PORT": 33062,
    # 商品配置
    "DUJIAOGOODS": {
        13: 30,  # id：天数
        14: 365,
    }
}
