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
    user_code: str
    created_at: Optional[datetime] = None
    carid: Optional[str] = None
    is_plus: Optional[int] = None
    expiration_date: Optional[datetime] = None
    email: Optional[str] = None
    auto_car: Optional[int] = None
    state: Optional[int] = None
    remark: Optional[str] = None
    xy_id: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True


class ShareCar(BaseModel):
    """
    车数据模型
    """
    created_at: Optional[datetime] = None
    carid: Optional[str] = None
    car_type: Optional[int] = None
    max_user_num: Optional[int] = None
    state: Optional[int] = None
    plus_ex_time: Optional[datetime] = None
    remark: Optional[str] = None
    xy_id: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    sess: Optional[str] = None
    updated_at: Optional[datetime] = None
    real_time_state: Optional[str] = None
    tag: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True


class ShareConfig(BaseModel):
    """
    配置数据模型
    """
    key: Optional[str] = None
    value: Optional[str] = None
    created_at: Optional[datetime] = None
    remark: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True


class Order(BaseModel):
    """
    订单数据模型
    """
    platform: Optional[str] = None
    order_id: Optional[str] = None
    duration: Optional[int] = None
    is_plus: Optional[int] = None
    is_exclusive: Optional[int] = None
    created_at: Optional[datetime] = None
    email: Optional[str] = None
    state: Optional[int] = None
    remark: Optional[str] = None
    tag: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True
