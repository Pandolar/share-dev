# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : data_model.py
# @Time : 2024/1/19 14:08
# -------------------------------

from datetime import datetime
from pydantic import BaseModel
from typing import  Optional

class ShareUser(BaseModel):
    """
    用户数据模型
    """
    user_code: str
    nickname: Optional[str] = None
    carid: Optional[str] = None
    is_plus: Optional[int] = None
    expiration_date: Optional[datetime] = None
    email: Optional[str] = None
    auto_car: Optional[int] = None
    state: Optional[int] = None
    remark: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True


class ShareCar(BaseModel):
    """
    车数据模型
    """
    carid: Optional[str] = None
    car_type: Optional[int] = None
    max_user_num: Optional[int] = None
    state: Optional[int] = None
    plus_ex_time: Optional[datetime] = None
    remark: Optional[str] = None

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




# class StandardResponse(BaseModel):
#     status: int
#     message: str
#     data: Optional[Any] = None
