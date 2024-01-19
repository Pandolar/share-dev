# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : app.py
# @Time : 2024/1/18 17:04
# -------------------------------
from fastapi import FastAPI,Response


from scr.myapi import MyApi
from models import ShareUser, ShareCar, ShareConfig, ShareUserDB
from tools import Tools

app = FastAPI()
my_api = MyApi()


# 获取全部用户信息
@app.get("/share/get_user_all_info")
async def get_all_info():
    return Tools().ret_data(my_api.get_all_info())


# 获取某用户信息
@app.get("/share/get_user_info")
async def get_user_info(user_code):
    return Tools().ret_data(my_api.get_user_info(user_code))


# 增加用户信息
@app.post("/share/add_user_info")
async def add_info(item: ShareUser):
    db_item = ShareUserDB(**item.dict())
    data = my_api.add_info(db_item)
    return Tools().ret_data(data)


# 更新某用户信息
@app.post("/share/update_user_info")
async def update_info(item: ShareUser):
    # 转成pydantic模型
    pyd_item = Tools().convert_sqlalchemy_to_pydantic(item, ShareUser)
    date = my_api.update_user_info(pyd_item)
    return Tools().ret_data(date)







# 重定向跳转链接
@app.get("/jump")
async def jump(user_code, response: Response):
    url = my_api.jump_url(user_code)
    response.status_code = 307  # 临时重定向
    response.headers["Location"] = url
    return response
