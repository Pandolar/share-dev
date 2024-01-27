# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : mydb.py
# @Time : 2024/1/26 11:16
# -------------------------------
from sqlalchemy import create_engine
from sqlalchemy import inspect
from models import ShareUserDB, ShareCarDB, ShareConfigDB, ShareUser, ShareCar, ShareConfig, OrderDB
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import CONFIG


class DataBase():
    """
    数据库操作类
    """

    def __init__(self, logger):
        """
        初始化
        :param config:
        """
        config = CONFIG
        self.host = config['DB_HOST']
        self.user = config['DB_USER']
        self.password = config['DB_PASSWORD']
        self.database = config['DB_NAME']
        self.port = config['DB_PORT']
        self.SHARE_HOST = config['SHARE_HOST']
        # self.SHORT_URL_PREFIX = config['SHORT_URL_PREFIX']
        self.RANDOM_SUFFIX_LENGTH = config['MAX_USER_IN_CAR']
        # self.DATABASE_URL = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}"
        self.DATABASE_URL = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.logger = logger
        # 创建 SQLAlchemy 引擎
        try:
            self.engine = create_engine(self.DATABASE_URL)

            # 创建 Session 工厂
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.schema = self.database
            self.logger.info(f'数据库连接成功')
        except Exception as e:
            self.logger.error(f'数据库连接失败 {e}')

    def get_engine(self):
        """
        获取引擎
        :return:
        """
        return self.engine

    def is_table(self) -> bool:
        """
        检查 表是否存在
        :return: bool
        """
        inspector = inspect(self.engine)
        # 传递数据库模式名称
        tables = inspector.get_table_names(schema=self.schema)
        return len(tables) > 0

    def create_table(self):
        """
        创建表。
        :return:
        """
        if not self.is_table():
            # Base.metadata.create_all(self.engine)
            # 创建全部表
            ShareUserDB.__table__.create(self.engine)
            ShareCarDB.__table__.create(self.engine)
            # ShareConfigDB.__table__.create(self.engine)
            OrderDB.__table__.create(self.engine)
            self.logger.info(f'成功创建数据表')
            # 写入初始数据
            self.write_beginning_data()
        else:
            self.logger.info(f'数据表已存在，无需创建')

    def write_beginning_data(self):
        """
        写入初始数据
        :return:
        """
        with self.SessionLocal() as db:
            try:
                # 写入初始数据
                db.add(ShareUserDB(user_code='zhangsan', nickname='张三', carid='a123456',
                                   is_plus=1, expiration_date=datetime.now(), state=1, email='123@qq.com', remark='示例用户'))
                db.add(ShareCarDB(carid='car123456', car_type=1, state=1, plus_ex_time=datetime.now()), remark='示例车辆')
                db.add(ShareConfigDB(key='test', value='test01', remark='示例配置'))
                db.commit()
                self.logger.info(f'成功写入示例数据')
            except Exception as e:
                db.rollback()
                self.logger.info(f'写入示例数据失败 {e}')
