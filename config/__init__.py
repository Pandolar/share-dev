# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : __init__.py.py
# @Time : 2024/1/18 15:32
# -------------------------------
CONFIG = {
    # 数据库配置
    "DB_HOST": "127.0.0.1",
    "DB_USER": "share_dev",
    "DB_PASSWORD": "share_dev",
    "DB_NAME": "share_dev",
    "DB_PORT": 33062,
    "DEFAULT_REDIRECT_URL": "go.foxaigc.com",  # share主地址
    #"SHORT_URL_PREFIX": "https://s.foxaigc.com/share/",  # 短链接前缀
    "RANDOM_SUFFIX_LENGTH": 5,  # 随机生成的短链接后缀长度
    "PORT": 18980,  # FastAPI 服务端口号
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
