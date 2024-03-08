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
    用户表
    """
    __tablename__ = 'share_user'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    xy_user_id = Column(String(255, collation="utf8mb4_general_ci"), unique=True, comment='xy_id')
    username = Column(String(60, collation="utf8mb4_general_ci"), unique=True, nullable=False, comment='用户授权码/昵称')
    email = Column(String(255, collation="utf8mb4_general_ci"), comment='邮箱', unique=True)
    password = Column(String(255, collation="utf8mb4_general_ci"), comment='密码')
    normal_ex_time = Column(DateTime, comment='普通到期时间')
    gold_ex_time = Column(DateTime, comment='黄金到期时间')
    diamond_ex_time = Column(DateTime, comment='钻石到期时间')
    carid = Column(String(255, collation="utf8mb4_general_ci"), comment='车号')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    state = Column(Integer, comment='状态0被封 1正常')
    remark = Column(String(1024, collation="utf8mb4_general_ci"), comment='备注')
    aff_code = Column(String(255, collation="utf8mb4_general_ci"), comment='邀请码')
    tag = Column(String(255, collation="utf8mb4_general_ci"), comment='标签')


class ShareCarDB(Base):
    """
    车表数据模型
    """
    __tablename__ = 'share_car'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    xy_car_id = Column(String(255, collation="utf8mb4_general_ci"), unique=True, nullable=False, comment='车号')
    car_type = Column(Integer, comment='状态0是3.5，1是plus号')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    # 更新时间
    updated_at = Column(DateTime, server_default=func.now(), comment='更新时间')
    # 邮箱
    email = Column(String(255, collation="utf8mb4_general_ci"), comment='邮箱')
    # 密码
    password = Column(String(255, collation="utf8mb4_general_ci"), comment='密码')
    # session
    sess = Column(TEXT(), comment='sess')
    state = Column(Integer, comment='状态0被封 1正常')
    plus_ex_time = Column(DateTime, comment='plus到期时间', default=Tools.add_day)
    remark = Column(String(1024, collation="utf8mb4_general_ci"), comment='备注')
    tag = Column(String(255, collation="utf8mb4_general_ci"), comment='标签')


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
    type = Column(Integer, comment='类型')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    email = Column(String(255, collation="utf8mb4_general_ci"), comment='邮箱')
    user_id = Column(Integer, comment='用户id')
    state = Column(Integer, comment='状态0被封 1正常')
    remark = Column(String(1024, collation="utf8mb4_general_ci"), comment='备注')

class PackageDB(Base):
    """
    套餐表数据模型
    """
    __tablename__ = 'package'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255, collation="utf8mb4_general_ci"), unique=True, nullable=False, comment='套餐名')
    describe = Column(String(255, collation="utf8mb4_general_ci"), comment='描述')
    type = Column(Integer, comment='类型')
    duration = Column(Integer, comment='时长，单位天')
    state = Column(Integer, comment='状态')
    remark = Column(String(1024, collation="utf8mb4_general_ci"), comment='备注')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')