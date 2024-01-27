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
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from datetime import datetime
from src.log import logger
from sqlalchemy.ext.declarative import declarative_base
from config import CONFIG
from models import ShareUserDB, ShareCarDB, ShareConfigDB, ShareUser, ShareCar, ShareConfig
from tools import Tools
from src.mydb import DataBase
from src.myredis import share_redis
from xy_share_api import Xyhelper

Base = declarative_base()

app = FastAPI()
xyhelper = Xyhelper()

class MyApi():
    def __init__(self):
        database = DataBase()
        database.create_table()
        self.redis = share_redis
        self.engine = database.get_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @contextmanager
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    # ---------------用户相关---------------
    def get_all_user_info(self):
        """
        获取所有信息
        :param db:
        :return:
        """
        with self.get_db() as db:  # 使用 with 语句来管理数据库会话
            result = db.query(ShareUserDB).all()  # 在 with 块内进行查询
            logger.info(f'获取所有信息成功')
            # 过滤出全部的时间字段 全部转为字符串 的“2024-01-03 00:00:00”格式
            result = [i.__dict__ for i in result]
            for i in result:
                for k, v in i.items():
                    if isinstance(v, datetime):
                        i[k] = v.strftime('%Y-%m-%d %H:%M:%S')
            return result

    def add_user_info(self, item: ShareUser):
        """
        添加信息
        :return:
        """
        # 先添加到xy
        # xyhelper.add_user(item.user_code, item.remark, item.expiration_date)
        with self.get_db() as db:
            try:
                db.add(item)
                db.commit()
                # 如果item为多个对象，需要遍历
                if isinstance(item, list):
                    for i in item:
                        logger.info(f'添加用户{i.user_code}成功')
                return 'ok'
            except Exception as e:
                db.rollback()
                logger.info(f'添加用户失败')
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

    def delete_user_info(self, user_code):
        # 删除某用户信息
        if user_code:
            with self.get_db() as db:
                try:
                    db.query(ShareUserDB).filter(ShareUserDB.user_code == user_code).delete()
                    db.commit()
                    msg = f'删除用户{user_code}信息成功'
                    logger.info(msg)
                    return msg
                except Exception as e:
                    db.rollback()
                    msg = f'error: 删除用户{user_code}信息失败 {e}'
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

    # ---------------车辆相关---------------
    def get_all_car_info(self):
        """
        获取所有信息
        :param db:
        :return:
        """
        with self.get_db() as db:
            result = db.query(ShareCarDB).all()
            logger.info(f'获取所有信息成功')
            # 过滤出全部的时间字段 全部转为字符串 的“2024-01-03 00:00:00”格式
            result = [i.__dict__ for i in result]
            for i in result:
                for k, v in i.items():
                    if isinstance(v, datetime):
                        i[k] = v.strftime('%Y-%m-%d %H:%M:%S')
            return result

    def add_car_info(self, item: ShareCar):
        """
        添加信息
        :return:
        """
        with self.get_db() as db:
            try:
                db.add(item)
                db.commit()
                # 如果item为多个对象，需要遍历
                if isinstance(item, list):
                    for i in item:
                        logger.info(f'添加车辆{i.carid}成功')
                return 'ok'
            except Exception as e:
                db.rollback()
                logger.info(f'添加车辆失败')
                return f'error: {e}'

    def update_car_info(self, item: ShareCar):
        # 更新信息
        if item.carid:
            with self.get_db() as db:
                try:
                    update_data = item.dict(exclude_unset=True)
                    db.query(ShareCarDB).filter(ShareCarDB.carid == item.carid).update(update_data)
                    db.commit()
                    msg = f'更新车辆{item.carid}成功'
                    logger.info(msg)
                    return msg
                except Exception as e:
                    db.rollback()
                    msg = f'error: 更新车辆{item.carid}失败 {e}'
                    logger.info(msg)
                    return msg
        else:
            return 'error: no carid'

    def get_car_info(self, carid):
        # 获取车辆信息
        if carid:
            with self.get_db() as db:
                try:
                    result = db.query(ShareCarDB).filter(ShareCarDB.carid == carid).first()
                    # 转换成pydantic模型
                    ret_ = ShareCar(**result.__dict__)
                    msg = f'获取车辆{carid}信息成功'
                    logger.info(msg)
                    return ret_
                except Exception as e:
                    msg = f'error: 获取车辆{carid}信息失败 {e}'
                    logger.info(msg)
                    return msg
        else:
            return 'error: no carid'

    def delete_car_info(self, carid):
        # 删除某车辆信息
        if carid:
            with self.get_db() as db:
                try:
                    db.query(ShareCarDB).filter(ShareCarDB.carid == carid).delete()
                    db.commit()
                    msg = f'删除车辆{carid}信息成功'
                    logger.info(msg)
                    return msg
                except Exception as e:
                    db.rollback()
                    msg = f'error: 删除车辆{carid}信息失败 {e}'
                    logger.info(msg)
                    return msg
        else:
            return 'error: no carid'

    # ---------------初始化同步信息相关---------------
    def filter_delete(self, data: list):
        # 过滤掉已经删除的用户
        ret = []
        for i in data:
            if i["deleted_at"] is None:
                ret.append(i)
        return ret

    def sync_xy_user(self):
        # 首次同步xy用户
        try:
            # 先使用xy 的api拿到所有用户信息

            xy_dict = xyhelper.user_page(1, 10000)
            print(xy_dict['code'])
            if xy_dict['code'] == 1000:
                xy_user_list = xy_dict['data']['list']
                # 将xy用户信息写入数据库
                # 先清空share_user和share_car表
                with self.get_db() as db:
                    try:
                        db.query(ShareUserDB).delete()
                        sql = text(f'alter table {ShareUserDB.__tablename__} AUTO_INCREMENT=1;')
                        db.execute(sql)
                        db.commit()
                        logger.info(f'清空share_user表成功')
                    except Exception as e:
                        db.rollback()
                        print(e)
                        logger.info(f'清空share_user表失败 {e}')
                        return {'msg': f'error 清空share_user表失败 {e}'}
                # 写入share_user表
                for xy_user in self.filter_delete(xy_user_list):
                    # 转换成ShareUserDB模型
                    # 先对齐字段
                    #  xy的数据示例{'createTime': '2024-01-16 11:08:41', 'deleted_at': None, 'expireTime': '2024-01-20 00:00:00', 'id': 2, 'isPlus': 1, 'remark': 'vip user 1', 'updateTime': '2024-01-17 10:27:34', 'userToken': 'vip1'}
                    xy_add_user = {}
                    xy_add_user['user_code'] = xy_user['userToken']
                    # xy_add_user['nickname'] = xy_user['remark']
                    # xy_add_user['carid'] = xy_user['remark']
                    xy_add_user['is_plus'] = xy_user['isPlus']
                    xy_add_user['expiration_date'] = xy_user['expireTime']
                    # xy_add_user['email'] = xy_user['remark']
                    xy_add_user['auto_car'] = 0
                    xy_add_user['state'] = 1
                    xy_add_user['remark'] = xy_user['remark']
                    xy_add_user['xy_id'] = xy_user['id']
                    user = ShareUserDB(**xy_add_user)
                    # 写入数据库
                    self.add_user_info(user)
                logger.info(f'写入share_user表成功')
                return {'msg': 'ok'}

            else:
                return {'msg': xy_dict['message'], 'code': xy_dict['code']}
        except Exception as e:
            logger.info(f'获取xy用户信息失败 {e}')
            return {'msg': f'获取xy用户信息失败 {e}'}

    def sync_xy_car(self):
        # 首次同步xy车辆
        try:
            # 先使用xy 的api拿到所有车辆信息
            xyhelper = Xyhelper()
            xy_dict = xyhelper.session_page(1, 10000)
            if xy_dict['code'] == 1000:
                xy_car_list = xy_dict['data']['list']
                # 将xy车辆信息写入数据库
                # 先清空share_car表
                with self.get_db() as db:
                    try:
                        db.query(ShareCarDB).delete()
                        db.execute(text(f'alter table {ShareCarDB.__tablename__} AUTO_INCREMENT=1;'))
                        db.commit()
                        logger.info(f'清空share_car表成功')
                    except Exception as e:
                        db.rollback()
                        logger.info(f'清空share_car表失败 {e}')
                # 写入share_car表
                for xy_car in self.filter_delete(xy_car_list):
                    # 转换成ShareCarDB模型
                    # 先对齐字段
                    # xy的数据示例{"code": 1000, "message": "BaseResMessage", "data": {"list": [{"carID": "54jymsbn", "createTime": "2024-01-09 16:36:45", "deleted_at": null, "email": "heiwailetchthipa@mail.com", "id": 3, "isPlus": 1, "officialSession": "xxx", "accessToken":"xxx", "password": "Ud1NyknvyJm1", "remark": "正规号1", "status": 1, "updateTime": "2024-01-26 11:52:49"}], "pagination": {"page": 1, "size": 1, "total": 88}}}
                    xy_add_car = {}
                    xy_add_car['carid'] = xy_car['carID']
                    xy_add_car['car_type'] = xy_car['isPlus']
                    xy_add_car['max_user_num'] = CONFIG['MAX_USER_IN_CAR']
                    xy_add_car['state'] = xy_car['status']
                    xy_add_car['email'] = xy_car['email']
                    xy_add_car['password'] = xy_car['password']
                    xy_add_car['sess'] = xy_car['officialSession']
                    xy_add_car['xy_id'] = xy_car['id']
                    xy_add_car['remark'] = xy_car['remark']
                    xy_add_car['updated_at'] = xy_car['updateTime']

                    car = ShareCarDB(**xy_add_car)
                    # 写入数据库
                    self.add_user_info(car)
                logger.info(f'写入share_car表成功')
                return {'msg': 'ok'}
        except Exception as e:
            logger.info(f'获取xy car信息失败 {e}')
            return {'msg': f'获取xy car信息失败 {e}'}

    # ---------------登陆和前端相关---------------
    def get_share_html(self):
        with open('html/home.html', 'r', encoding='utf-8') as html_file:
            pagetxt = html_file.read()

        # page = pagetxt.format(base_url=SHARE_HOST)
        page = pagetxt
        return HTMLResponse(page)

    def get_login_html(self):
        with open('html/login.html', 'r', encoding='utf-8') as html_file:
            pagetxt = html_file.read()
        # page = pagetxt.format(base_url=SHARE_HOST)
        page = pagetxt
        return HTMLResponse(page)

    def get_token(self, user, password):
        if user == CONFIG['USER'] and password == CONFIG['PASSWORD']:
            token = Tools().generation_token()
            # 写入redis

            self.redis.set_redis('share-2-token', token, 24 * 60 * 60)  # 24小时过期
            return {'token': token, 'msg': 'ok'}
        else:
            return {'msg': 'error 用户名或密码错误'}

    # ---------------其他接口---------------
    def jump_url(self, user_code, is_https=False, host=CONFIG['SHARE_HOST']):
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