# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : myapi.py
# @Time : 2024/1/18 15:33
# -------------------------------
import json

from fastapi import FastAPI, HTTPException, Response, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import inspect
from scr.log import Logger
from sqlalchemy import Column, Integer, String, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from config import CONFIG

Base = declarative_base()
logger = Logger('share_dev').get_logger()
app = FastAPI()


class share_dev(Base):
    """
    数据表数据模型
    """
    __tablename__ = CONFIG['DB_NAME']
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_code = Column(String(60, collation="utf8mb4_general_ci"), unique=True, nullable=False, comment='用户授权码')
    nickname = Column(String(255, collation="utf8mb4_general_ci"), nullable=False, comment='昵称')
    carid = Column(String(255, collation="utf8mb4_general_ci"), comment='车号')
    is_plus = Column(Integer, comment='是否为plus')
    # long_url = Column(String(2048, collation="utf8mb4_general_ci"), nullable=False, comment='完整的跳转url')
    expiration_date = Column(DateTime, comment='到期时间')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    email = Column(String(255, collation="utf8mb4_general_ci"), comment='邮箱')
    auto_car = Column(Integer, comment='是否自动换车')
    state = Column(Integer, comment='状态0被封 1正常')

class ShareDevCreate(BaseModel):
    """
    创建短链接请求数据模型
    """
    user_code: str
    nickname: str
    carid: str
    is_plus: int
    # long_url: str
    expiration_date: datetime
    email: str
    auto_car: int
    state: int


class DataBase():
    """
    请求数据模型
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
        self.SHORT_URL_PREFIX = config['SHORT_URL_PREFIX']
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
        检查 share_dev 表是否存在
        :return: bool
        """
        inspector = inspect(self.engine)
        # 传递数据库模式名称
        tables = inspector.get_table_names(schema=self.schema)
        return CONFIG['DB_NAME'] in tables


    def create_table(self):
        """
        创建 share_dev 表。
        :return:
        """
        if not self.is_table():
            Base.metadata.create_all(self.engine)
            logger.info(f'成功创建 {CONFIG["DB_NAME"]} 表')
        else:
            logger.info(f'表 {CONFIG["DB_NAME"]} 已存在，无需创建')



class MyApi():
    def __init__(self):
        database=DataBase()
        database.create_table()
        self.engine = database.get_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    async def get_all_info(self, db: Session):
        """
        获取所有信息
        :param db:
        :return:
        """
        result = db.query(share_dev).all()
        logger.info(f'获取所有信息成功')
        return result

    async def add_info(self, item: ShareDevCreate, db: Session = Depends(get_db)):
        """
        添加信息
        :return:
        """
        try:
            db.add(item)
            db.commit()
            db.close()
            logger.info(f'添加用户{item.user_code}成功')
            return 'ok'
        except Exception as e:
            db.rollback()
            db.close()
            logger.info(f'添加用户{item.user_code}失败')

            return 'error'

    async def update_user_info(self, item: ShareDevCreate, db: Session = Depends(get_db)):
        # 更新信息
        if item.user_code:
            try:
                # update_data = item.dict(exclude_unset=True)
                db.query(share_dev).filter(share_dev.user_code == item.user_code).update(ShareDevCreate)
                db.commit()
                db.close()
                logger.info(f'更新用户{item.user_code}成功')
                return 'ok'
            except Exception as e:
                db.rollback()
                db.close()
                logger.info(f'更新用户{item.user_code}失败')
                return 'error'
        else:
            return 'no user_code'

    async def sealing_info(self, item: ShareDevCreate, db: Session = Depends(get_db)):
        # 封禁用户信息的逻辑
        if item.user_code:
            try:
                db.query(share_dev).filter(share_dev.user_code == item.user_code).update({share_dev.state: 1})
                db.commit()
                db.close()
                logger.info(f'封禁用户{item.user_code}成功')
                return 'ok'
            except Exception as e:
                db.rollback()
                db.close()
                logger.info(f'封禁用户{item.user_code}失败')
                return 'error'
    async def get_user_info(self, user_code, db: Session = Depends(get_db)):
        # 获取用户信息
        if user_code:
            try:
                result = db.query(share_dev).filter(share_dev.user_code == user_code).first()
                if result:
                    return result
                else:
                    return 'no user_code'
            except Exception as e:
                logger.info(f'获取用户信息失败')
                return 'error'
        else:
            return 'no user_code'

    async def is_out_time(self, user_code, db: Session = Depends(get_db)):
        # 判断是否过期
        if user_code:
            try:
                result = db.query(share_dev).filter(share_dev.user_code == user_code).first()
                if result:
                    if result.expiration_date > datetime.now():
                        return {'is_out_time': False, 'user_code': user_code, 'expiration_date': result.expiration_date}
                    else:
                        return {'is_out_time': True, 'user_code': user_code, 'expiration_date': result.expiration_date}
                else:
                    return {'is_out_time': True, 'user_code': "no user_code"}
            except Exception as e:
                logger.info(f'判断是否过期失败')
                return  {'is_out_time': False}
        else:
            return {'is_out_time': True, 'user_code': "no user_code"}

    async def jump_url(self, response: Response, host, user_code, carid, is_https=False, db: Session = Depends(get_db)):
        # 获取跳转url 重定向
        ret_ = await self.is_out_time(user_code, db)
        if ret_['is_out_time']:
            # 过期
            return {'msg': '过期 or 不存在'}
        else:
            # 未过期
            http = 'https' if is_https else 'http'
            url = f'{http}://{host}/auth/logintoken?carid={carid}&usertoken={user_code}'
            response.status_code = 307  # 临时重定向
            response.headers["Location"] = url
            return response

    async def get_share_html(self):
        with open('html/list.html', 'r', encoding='utf-8') as html_file:
            pagetxt = html_file.read()

        # page = pagetxt.format(base_url=DEFAULT_REDIRECT_URL)
        page = pagetxt
        return HTMLResponse(page)