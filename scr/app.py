# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : app.py
# @Time : 2024/1/18 17:04
# -------------------------------
from fastapi import FastAPI, Depends
from scr.myapi import MyApi,ShareDevCreate
from sqlalchemy.orm import Session
# 导入其他所需模块，如 MyAPI, YourItemModel 等

app = FastAPI()
my_api = MyApi()
# 获取全部信息
@app.get("/share/get_all_info")
async def get_all_info():
    return await my_api.get_all_info()
# 增加信息
@app.post("/share/add_info")
async def add_info(item: ShareDevCreate):
    return await my_api.add_info(item)

# 更新某用户信息
@app.post("/share/update_info")
async def update_info(item: ShareDevCreate):
    return await my_api.update_user_info(item)

