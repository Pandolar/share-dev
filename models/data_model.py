# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : data_model.py
# @Time : 2024/1/19 14:08
# -------------------------------

from datetime import datetime
from pydantic import BaseModel
from typing import Optional


# 数据模型

class ShareUser(BaseModel):
    """
    用户数据模型
    """
    created_at: Optional[datetime] = None
    xy_user_id: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    normal_ex_time: Optional[datetime] = None
    gold_ex_time: Optional[datetime] = None
    diamond_ex_time: Optional[datetime] = None
    carid: Optional[str] = None
    state: Optional[int] = None
    remark: Optional[str] = None
    aff_code: Optional[str] = None
    tag: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True


class ShareCar(BaseModel):
    """
    车数据模型
    """
    xy_car_id: Optional[str] = None
    car_type: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    email: Optional[str] = None
    password: Optional[str] = None
    sess: Optional[str] = None
    state: Optional[int] = None
    plus_ex_time: Optional[datetime] = None
    remark: Optional[str] = None
    tag: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True


class ShareConfig(BaseModel):
    """
    配置数据模型
    """
    created_at: Optional[datetime] = None
    key: Optional[str] = None
    value: Optional[str] = None
    remark: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True


class Order(BaseModel):
    """
    订单数据模型
    """
    created_at: Optional[datetime] = None
    name: Optional[str] = None
    describe: Optional[str] = None
    duration: Optional[int] = None
    type: Optional[int] = None
    state: Optional[int] = None
    remark: Optional[str] = None
    class Config:
        orm_mode = True
        from_attributes = True
