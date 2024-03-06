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
from sqlalchemy import text, and_, or_
from datetime import datetime
from src.log import logger
from sqlalchemy.ext.declarative import declarative_base
from config import CONFIG
from models import ShareUserDB, ShareCarDB, ShareConfigDB, ShareUser, ShareCar, ShareConfig
from tools import Tools
from src.mydb import DataBase
from src.myredis import share_redis
from xy_share_api import Xyhelper
import random

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

    def add_user_info(self, item: ShareUser, to_xy=False):
        """
        添加信息
        :return:
        """
        # 先添加到xy
        if to_xy:
            expire_time_str = item.expiration_date.strftime('%Y-%m-%d %H:%M:%S')
            xy_ret = xyhelper.add_user(item.user_code, expire_time_str, item.is_plus)
            if not xy_ret['code']:
                return {'msg': f'error xy源数据库添加失败{xy_ret["msg"]}'}
        with self.get_db() as db:
            try:
                if to_xy:
                    xy_id = xy_ret['data']['data']['id']
                    item.xy_id = xy_id
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
            xy_ret = xyhelper.user_update(
                createTime=item.created_at,
                expireTime=item.expireTime,
                id=item.xy_id,
                isPlus=item.is_plus,
                remark=item.remark,
                updateTime=item.updateTime,
                userToken=item.user_code
            )
            if xy_ret['code'] is False:
                return f'error xy源数据库更新失败{xy_ret["msg"]}'
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

    def delete_user_info(self, user_code: list):
        # 删除某用户信息
        if len(user_code):
            # 先根据user_code获取xy_id
            # xy_id_list = []
            # for i in user_code:
            #     xy_id_list.append(self.get_user_info(i).xy_id)
            # xyhelper.delete_user(xy_id_list)

            with self.get_db() as db:
                try:
                    result = db.query(ShareUserDB.xy_id).filter(ShareUserDB.user_code.in_(user_code)).all()
                    xy_id_list = []
                    for i in result:
                        if i[0] != '':
                            xy_id_list.append(i[0])

                    xy_ret = xyhelper.delete_user(xy_id_list)
                    if xy_ret['code'] is False:
                        msg = f'error xy源数据库删除失败{xy_ret["msg"]}'
                        logger.info(msg)
                        return msg
                    db.query(ShareUserDB).filter(ShareUserDB.user_code.in_(user_code)).delete(synchronize_session=False)
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

    def add_car_info(self, item: ShareCar, to_xy=False):
        """
        添加信息
        :return:
        """
        xy_status = True
        if to_xy:
            xy_ret = xyhelper.session_add(
                carID=item.carid,
                email=item.email,
                isPlus=item.car_type,
                password=item.password,
                remark=item.remark,
                status=item.state)
            if not xy_ret['code']:
                msg = f'error xy源数据库添加失败{xy_ret["msg"]}'
                logger.info(msg)
                xy_status = False
            all_info = self.get_all_car_info()
            for i in all_info:
                if i['carid'] == item.carid:
                    xy_id = i['id']
        with self.get_db() as db:
            try:
                if to_xy:
                    item.xy_id = xy_id
                db.add(item)
                db.commit()
                # 如果item为多个对象，需要遍历
                if isinstance(item, list):
                    for i in item:
                        logger.info(f'添加车辆{i.carid}成功')
                if xy_status:
                    return 'ok'
                else:
                    return msg
            except Exception as e:
                db.rollback()
                logger.info(f'添加车辆失败')
                return f'error: {e}'

    def update_car_info(self, item: ShareCar):
        # 更新信息
        if item.carid:
            xy_ret = xyhelper.session_update(
                carID=item.carid,
                createTime=item.created_at,
                email=item.email,
                id=item.xy_id,
                isPlus=item.car_type,
                officialSession=item.sess,
                password=item.password,
                remark=item.remark,
                status=item.state,
                updateTime=item.updated_at
            )
            if xy_ret['code'] is False:
                return f'error xy源数据库更新失败{xy_ret["msg"]}'

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

            xy_ret = xyhelper.user_page(1, 10000)
            if xy_ret['code'] is False:
                msg = f'error xy源数据库获取失败{xy_ret["msg"]}'
                logger.info(msg)
                return msg
            else:
                xy_dict = xy_ret['data']
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
                    if xy_user['remark'] and '妹子' in xy_user['remark']:
                        print(xy_add_user)
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

            xy_ret = xyhelper.session_page(1, 10000)
            if xy_ret['code'] is False:
                msg = f'error xy源数据库获取失败{xy_ret["msg"]}'
                logger.info(msg)
                return msg
            else:
                xy_dict = xy_ret['data']
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
                    self.add_car_info(car)
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
    def jump_url(self, user_code, is_https=False, host=CONFIG['SHARE_HOST'], is_auto_car=False):
        # 获取跳转url 重定向
        # 这里详细逻辑后面写
        logger.info(f'获取跳转url: ' + user_code)
        ret_ = self.is_out_time(user_code)
        if ret_['is_out_time']:
            return {'msg': '过期  or 不存在'}
        else:
            # 未过期
            # 获取carid 从MySQL的share_user表查询
            if is_auto_car:
                # 先从数据库查出是否为plus
                with self.get_db() as db:  # 使用 with 语句来管理数据库会话
                    # result = db.query(ShareUserDB.is_plus).filter(ShareCarDB.user_code == user_code).first()
                    # 定义查询参数
                    user_code = str(user_code)
                    car_state = 1
                    real_time_state_keywords = ['推荐', '可用']

                    # 构造参数化查询
                    query = db.query(
                        ShareCarDB.carid,
                        ShareCarDB.real_time_state
                    ).join(
                        ShareUserDB, ShareUserDB.is_plus == ShareCarDB.car_type
                    ).filter(
                        ShareUserDB.user_code == user_code,
                        ShareCarDB.state == car_state,
                        or_(
                            *[ShareCarDB.real_time_state.like(f'%{keyword}%') for keyword in real_time_state_keywords]
                        )
                    )
                    results = query.all()

                    # 假设 results 是之前查询得到的结果
                    # results = [(123, '可用'), (456, '推荐'), ...]

                    # 首先筛选出包含 "推荐" 的记录
                    recommended = [carid for carid, state in results if '推荐' in state]

                    # 如果存在包含 "推荐" 的记录，从中随机选择一个
                    if recommended:
                        chosen_carid = random.choice(recommended)
                    else:
                        # 否则，从所有记录中选择一个包含 "可用" 的
                        available = [carid for carid, state in results if '可用' in state]
                        if available:
                            chosen_carid = random.choice(available)
                        else:
                            chosen_carid = None  # 如果没有符合条件的记录，返回 None

                    # chosen_carid 是最终选择的 carid
                    if not chosen_carid:
                        logger.info(f'获取跳转url失败: ' + user_code)
                        return None
                    else:
                        # return chosen_carid
                        url = Tools().get_url(host, user_code, chosen_carid, is_https=is_https)
                        logger.info(f'获取跳转url成功: ' + url)
                        return url
            else:
                carid = self.get_user_info(user_code).carid
                url = Tools().get_url(host, user_code, carid, is_https=is_https)
                logger.info(f'获取跳转url成功: ' + url)
                return url
