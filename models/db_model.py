# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : db_model.py
# @Time : 2024/1/19 14:07
# -------------------------------
from tools import Tools
from sqlalchemy import Column, Integer, String, DateTime,TEXT
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 数据库模型

class ShareUserDB(Base):
    """
    用户表数据模型
    """
    __tablename__ = 'share_user'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    xy_id = Column(String(255, collation="utf8mb4_general_ci"), unique=True, comment='xy_id')
    user_code = Column(String(60, collation="utf8mb4_general_ci"), unique=True, nullable=False, comment='用户授权码')
    # nickname = Column(String(255, collation="utf8mb4_general_ci"), comment='昵称')
    carid = Column(String(255, collation="utf8mb4_general_ci"), comment='车号')
    is_plus = Column(Integer, comment='是否为plus')
    expiration_date = Column(DateTime, comment='到期时间')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    email = Column(String(255, collation="utf8mb4_general_ci"), comment='邮箱')
    auto_car = Column(Integer, comment='是否自动换车')
    state = Column(Integer, comment='状态0被封 1正常')
    remark = Column(String(1024, collation="utf8mb4_general_ci"), comment='备注')


class ShareCarDB(Base):
    """
    车表数据模型
    """
    __tablename__ = 'share_car'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    carid = Column(String(255, collation="utf8mb4_general_ci"), unique=True, nullable=False, comment='车号')
    car_type = Column(Integer, comment='状态0是3.5，1是plus号')
    max_user_num = Column(Integer, comment='最大用户数')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    # 更新时间
    updated_at = Column(DateTime, server_default=func.now(), comment='更新时间')
    # 邮箱
    email = Column(String(255, collation="utf8mb4_general_ci"), comment='邮箱')
    # 密码
    password = Column(String(255, collation="utf8mb4_general_ci"), comment='密码')
    # session
    sess = Column(TEXT(), comment='sess')
    # xy_id
    xy_id = Column(String(255, collation="utf8mb4_general_ci"), comment='xy_id')
    real_time_state = Column(String(255, collation="utf8mb4_general_ci"), comment='实时状态')
    state = Column(Integer, comment='状态0被封 1正常')
    plus_ex_time = Column(DateTime, comment='plus到期时间', default=Tools.add_day)
    remark = Column(String(1024, collation="utf8mb4_general_ci"), comment='备注')


class ShareConfigDB(Base):
    """
    配置表数据模型
    """
    __tablename__ = 'share_config'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    key = Column(String(255, collation="utf8mb4_general_ci"), unique=True, nullable=False, comment='键')
    value = Column(String(255, collation="utf8mb4_general_ci"), comment='值')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    remark = Column(String(1024, collation="utf8mb4_general_ci"), comment='备注')


class OrderDB(Base):
    """
    订单表数据模型
    """
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    platform = Column(String(255, collation="utf8mb4_general_ci"), unique=True, nullable=False, comment='平台')
    order_id = Column(String(255, collation="utf8mb4_general_ci"), unique=True, nullable=False, comment='订单号')
    duration = Column(Integer, comment='时长，单位天')
    is_plus = Column(Integer, comment='是否为plus')
    is_exclusive = Column(Integer, comment='是否为独享')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    email = Column(String(255, collation="utf8mb4_general_ci"), comment='邮箱')
    state = Column(Integer, comment='状态0被封 1正常')
    remark = Column(String(1024, collation="utf8mb4_general_ci"), comment='备注')
