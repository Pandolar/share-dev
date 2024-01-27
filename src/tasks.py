# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : tasks.py
# @Time : 2024/1/27 17:38
# -------------------------------
import threading
import time
import config
from models import ShareCarDB
from src.mydb import DataBase
from xy_share_api import Xyhelper
from src.log import logger


class Tasks():

    @staticmethod
    def check_refresh_availability(db):
        """
        定时刷新可用状态
        :return:
        """
        try:
            # 先从数据库中获取所有状态为1的车辆号
            start_time=time.time()
            # get_all_carid
            all_carid = db.get_all_carid()
            status_dict = {}
            if all_carid is False or len(all_carid)==0:
                logger.info('无车号 不刷新')
                return False
            for i in all_carid:
                xy = Xyhelper()
                # 获取实时状态
                real_time_state = xy.get_endpoint(i[0])
                if real_time_state:
                    if i[0] == 'car123456':
                        logger.info('只有示例数据 不进行刷新实时状态')
                        return False
                    status_dict[i[0]] = real_time_state['message']
                    time.sleep(0.1)
                else:
                    print(real_time_state)
                    continue

            # 更新数据库
            with db.SessionLocal() as db:
                try:
                    # 开始更新前的日志
                    logger.info('刷新实时状态：开始批量更新数据库')
                    for k, v in status_dict.items():
                        db.query(ShareCarDB).filter(ShareCarDB.carid == k).update({ShareCarDB.real_time_state: v})
                    db.commit()
                    logger.info('刷新实时状态：所有数据更新成功，已提交到数据库')
                except Exception as e:
                    db.rollback()
                    logger.error(f'刷新实时状态：更新失败，发生异常: {e}')
                    return False
            end_time = time.time()
            elapsed_time = end_time - start_time
            # print(f"函数运行时间：{elapsed_time}秒")
            logger.info(f"刷新实时状态：运行时间{elapsed_time}秒")
            return True

        except Exception as e:
            print(e)
            return False


class GoTasks():
    def __init__(self):
        self.db = DataBase()
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.run_tasks, daemon=True)
        logger.info('启动定时任务')
        self.thread.start()

    def run_tasks(self):
        while True:
            with self.lock:
                Tasks().check_refresh_availability(self.db)
            time.sleep(config.CONFIG['REAL_TIME_REFRESH_DURATION'])
