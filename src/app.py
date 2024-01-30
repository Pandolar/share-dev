# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : app.py
# @Time : 2024/1/18 17:04
# -------------------------------
from fastapi import FastAPI, Response, Cookie, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from src.myapi import MyApi
from models import ShareUser, ShareCar, ShareConfig, ShareUserDB
from tools import Tools

# 初始化fastapi
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许跨域的域名，* 代表所有域名 线上环境可以注释掉
    allow_credentials=True,  # 支持 cookie
    allow_methods=["*"],  # 允许使用的请求方法
    allow_headers=["*"]  # 允许携带的 Headers
)
# 初始化api
my_api = MyApi()


# 对外
# ---------------登陆和前端相关---------------
@app.get("/")
async def default(token: str = Cookie(None)):
    if Tools().verify_token(token) is False:
        return RedirectResponse(url='/login')
    else:
        return RedirectResponse(url='/home')


@app.get("/login")
async def login(token: str = Cookie(None)):
    # if Tools().verify_token(token):
    #     return RedirectResponse(url='/home')
    return my_api.get_login_html()


@app.get("/home")
async def home(token: str = Cookie(None)):
    if Tools().verify_token(token) is False:
        return RedirectResponse(url='/login')
    else:
        return my_api.get_share_html()


@app.post("/get_token")
async def get_token(request: Request):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')
    response = my_api.get_token(username, password)
    if response['msg'] == 'ok':
        ret_ = Tools().ret_data(response['token'])
        return ret_
    return Tools().ret_data(response['msg'])


# --------------用户相关---------------
# 获取全部用户信息
@app.get("/share/get_user_all_info")
async def get_all_info(token: str = Cookie(None)):
    # 校验token
    if Tools().verify_token(token) is False:
        return RedirectResponse(url='/home')
    return Tools().ret_data(my_api.get_all_user_info())


# 获取某用户信息
@app.get("/share/get_user_info")
async def get_user_info(user_code: str, token: str = Cookie(None)):
    if Tools().verify_token(token) is False:
        return RedirectResponse(url='/home')
    return Tools().ret_data(my_api.get_user_info(user_code))


# 增加用户信息
@app.post("/share/add_user_info")
async def add_info(item: ShareUser, token: str = Cookie(None)):
    if Tools().verify_token(token) is False:
        return RedirectResponse(url='/home')
    db_item = ShareUserDB(**item.dict())
    data = my_api.add_user_info(db_item)
    return Tools().ret_data(data)


# 更新某用户信息
@app.post("/share/update_user_info")
async def update_info(item: ShareUser, token: str = Cookie(None)):
    if Tools().verify_token(token) is False:
        return RedirectResponse(url='/home')
    # 转成pydantic模型
    pyd_item = Tools().convert_sqlalchemy_to_pydantic(item, ShareUser)
    date = my_api.update_user_info(pyd_item)
    return Tools().ret_data(date)


# 删除某用户信息
@app.post("/share/delete_user_info")
async def delete_info(user_code: str, token: str = Cookie(None)):
    if Tools().verify_token(token) is False:
        return RedirectResponse(url='/home')
    data = my_api.delete_user_info(user_code)
    return Tools().ret_data(data)


# --------------同步信息---------------
# 同步用户和car信息
@app.get("/share/sync_xy_info")
async def sync_info(token: str = Cookie(None)):
    if Tools().verify_token(token) is False:
        return RedirectResponse(url='/home')
    user_mgs = my_api.sync_xy_user()
    car_msg = my_api.sync_xy_car()
    if user_mgs['msg'] != 'ok':
        return Tools().ret_data("error 用户同步失败")
    elif car_msg['msg'] != 'ok':
        return Tools().ret_data("error car同步失败")
    else:
        return Tools().ret_data('ok 同步成功')


# --------------车辆相关---------------
@app.get("/share/get_car_all_info")
async def get_car_all_info(token: str = Cookie(None)):
    if Tools().verify_token(token) is False:
        return RedirectResponse(url='/home')
    return Tools().ret_data(my_api.get_all_car_info())


@app.get("/share/get_car_info")
async def get_car_info(car_id: str, token: str = Cookie(None)):
    if Tools().verify_token(token) is False:
        return RedirectResponse(url='/home')
    return Tools().ret_data(my_api.get_car_info(car_id))


@app.post("/share/add_car_info")
async def add_car_info(item: ShareCar, token: str = Cookie(None)):
    if Tools().verify_token(token) is False:
        return RedirectResponse(url='/home')
    db_item = ShareUserDB(**item.dict())
    data = my_api.add_car_info(db_item)
    return Tools().ret_data(data)


@app.post("/share/update_car_info")
async def update_car_info(item: ShareCar, token: str = Cookie(None)):
    if Tools().verify_token(token) is False:
        return RedirectResponse(url='/home')
    # 转成pydantic模型
    pyd_item = Tools().convert_sqlalchemy_to_pydantic(item, ShareCar)
    date = my_api.update_car_info(pyd_item)
    return Tools().ret_data(date)


@app.post("/share/delete_car_info")
async def delete_car_info(car_id: str, token: str = Cookie(None)):
    if Tools().verify_token(token) is False:
        return RedirectResponse(url='/home')
    data = my_api.delete_car_info(car_id)
    return Tools().ret_data(data)


# --------------其他接口---------------
# 重定向跳转链接
@app.get("/jump")
async def jump(user_code:str, response: Response):
    url = my_api.jump_url(user_code)
    response.status_code = 307  # 临时重定向
    response.headers["Location"] = url
    return response
