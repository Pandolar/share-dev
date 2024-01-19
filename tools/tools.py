# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : tools.py
# @Time : 2024/1/19 14:01
# -------------------------------
from datetime import datetime, timedelta


class Tools:
    """
    工具类
    """

    @staticmethod
    def add_day(date=None, days=365 * 50):
        """
        日期加天数
        :param date: 日期 默认为现在
        :param days: 天数 默认为50年
        :return:
        """
        if date is None:
            date = datetime.now()
        return date + timedelta(days=days)

    @staticmethod
    def convert_sqlalchemy_to_pydantic(db_model, pydantic_model_class):
        """
        sqlalchemy模型转pydantic模型
        :param db_model:
        :param pydantic_model_class:
        :return:
        """
        return pydantic_model_class.from_orm(db_model)

    @staticmethod
    def ret_data(data):
        """
        返回数据
        :param data:
        :param message:
        :param status:
        :return:
        """
        # 如果data是文本 且以error开头 则返回错误
        if isinstance(data, str) and data.startswith("error"):
            return {
                "status": 500,
                "message": data,
                "data": None
            }
        else:
            return {
                "status": 200,
                "message": 'success',
                "data": data
            }

    @staticmethod
    def get_url(host, user_code, carid, is_https=False):
        # 获取跳转url
        http = 'https' if is_https else 'http'
        url = f'{http}://{host}/auth/logintoken?carid={carid}&usertoken={user_code}'
        return url

    # async def get_share_html(self):
    #     with open('html/list.html', 'r', encoding='utf-8') as html_file:
    #         pagetxt = html_file.read()
    #
    #     # page = pagetxt.format(base_url=DEFAULT_REDIRECT_URL)
    #     page = pagetxt
    #     return HTMLResponse(page)
