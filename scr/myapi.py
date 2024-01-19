# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : myapi.py
# @Time : 2024/1/18 15:33
# -------------------------------
from contextlib import contextmanager
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import inspect
from scr.log import Logger
from sqlalchemy.ext.declarative import declarative_base
from config import CONFIG
from models import ShareUserDB, ShareCarDB, ShareConfigDB, ShareUser, ShareCar, ShareConfig
from tools import Tools

Base = declarative_base()
logger = Logger('share_dev').get_logger()
app = FastAPI()


class DataBase():
    """
    数据库操作类
    """

    def __init__(self):
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
        self.DEFAULT_REDIRECT_URL = config['DEFAULT_REDIRECT_URL']
        # self.SHORT_URL_PREFIX = config['SHORT_URL_PREFIX']
        self.RANDOM_SUFFIX_LENGTH = config['RANDOM_SUFFIX_LENGTH']
        # self.DATABASE_URL = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}"
        self.DATABASE_URL = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

        # 创建 SQLAlchemy 引擎
        try:
            self.engine = create_engine(self.DATABASE_URL)

            # 创建 Session 工厂
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.schema = self.database
            logger.info(f'数据库连接成功')
        except Exception as e:
            logger.error(f'数据库连接失败 {e}')

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
        return ('share_user' in tables) and ('share_car' in tables) and ('share_config' in tables)

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
            ShareConfigDB.__table__.create(self.engine)
            logger.info(f'成功创建数据表')
            # 写入初始数据
            self.write_beginning_data()
        else:
            logger.info(f'数据表已存在，无需创建')

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
                logger.info(f'成功写入示例数据')
            except Exception as e:
                db.rollback()
                logger.info(f'写入示例数据失败 {e}')


class MyApi():
    def __init__(self):
        database = DataBase()
        database.create_table()
        self.engine = database.get_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @contextmanager
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_all_info(self):
        """
        获取所有信息
        :param db:
        :return:
        """
        with self.get_db() as db:  # 使用 with 语句来管理数据库会话
            result = db.query(ShareUserDB).all()  # 在 with 块内进行查询
            logger.info(f'获取所有信息成功')
            return result

    def add_info(self, item: ShareUser):
        """
        添加信息
        :return:
        """
        with self.get_db() as db:
            try:
                db.add(item)
                db.commit()
                logger.info(f'添加用户{item.user_code}成功')
                return 'ok'
            except Exception as e:
                db.rollback()
                logger.info(f'添加用户{item.user_code}失败')
                return f'error: {e}'

    def update_user_info(self, item: ShareUser):
        # 更新信息
        if item.user_code:
            with self.get_db() as db:
                try:
                    update_data = item.dict(exclude_unset=True)
                    db.query(ShareUserDB).filter(ShareUserDB.user_code == item.user_code).update(update_data)
                    db.commit()
                    msg = f'更新用户{item.user_code}成功'
                    logger.info(msg)
                    return msg
                except Exception as e:
                    db.rollback()
                    msg = f'error: 更新用户{item.user_code}失败 {e}'
                    logger.info(msg)
                    return msg
        else:
            return 'error: no user_code'

    # def sealing_info(self, item: ShareUser):
    #     # 封禁用户信息的逻辑
    #     if item.user_code:
    #         with self.get_db() as db:
    #             try:
    #                 db.query(ShareUserDB).filter(ShareUserDB.user_code == item.user_code).update({ShareUserDB.state: 1})
    #                 db.commit()
    #                 msg = f'封禁用户{item.user_code}成功'
    #                 logger.info(msg)
    #                 return msg
    #             except Exception as e:
    #                 db.rollback()
    #                 msg = f'error: 封禁用户{item.user_code}失败 {e}'
    #                 logger.info(msg)
    #                 return msg
    #     else:
    #         return 'error: no user_code'

    def get_user_info(self, user_code):
        # 获取用户信息
        if user_code:
            with self.get_db() as db:
                try:
                    result = db.query(ShareUserDB).filter(ShareUserDB.user_code == user_code).first()
                    # ret_= tools().convert_sqlalchemy_to_pydantic(result, ShareUser)
                    # 转换成pydantic模型
                    ret_ = ShareUser(**result.__dict__)
                    msg = f'获取用户{user_code}信息成功'
                    logger.info(msg)
                    return ret_
                except Exception as e:
                    msg = f'error: 获取用户{user_code}信息失败 {e}'
                    logger.info(msg)
                    return msg
        else:
            return 'error: no user_code'

    def is_out_time(self, user_code):
        # 判断是否过期
        if user_code:
            with self.get_db() as db:
                try:
                    result = db.query(ShareUserDB).filter(ShareUserDB.user_code == user_code).first()
                    if result:
                        is_out_time = result.expiration_date <= datetime.now()
                        return {'is_out_time': is_out_time, 'user_code': user_code, 'expiration_date': result.expiration_date}
                    else:
                        return {'is_out_time': True, 'user_code': "no user_code"}
                except Exception as e:
                    logger.info(f'判断是否过期失败')
                    # return f'error: {e}'
                    return {'is_out_time': False, 'msg': f'error: {e}'}
        else:
            return {'is_out_time': True, 'user_code': "no user_code"}

    def jump_url(self, user_code, is_https=False, host=CONFIG['DEFAULT_REDIRECT_URL']):
        # 获取跳转url 重定向
        # 这里详细逻辑后面写
        ret_ = self.is_out_time(user_code)
        if ret_['is_out_time']:
            return {'msg': '过期  or 不存在'}
        else:
            # 未过期
            # 获取carid 从MySQL的share_user表查询
            carid = self.get_user_info(user_code).carid
            url = Tools().get_url(host, user_code, carid, is_https=is_https)
            return url
    def get_share_html(self):
        with open('html/list.html', 'r', encoding='utf-8') as html_file:
            pagetxt = html_file.read()

        # page = pagetxt.format(base_url=DEFAULT_REDIRECT_URL)
        page = pagetxt
        return HTMLResponse(page)
