# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : xyhelperapi.py
# @Time : 2024/1/18 15:33
# -------------------------------
import requests
import json

class Xyhelper:
    def __init__(self,host,api_key):
        # host ="xxxx.com"
        # api_key = "xxxx"
        self.BASE_URL = f"http://{host}/adminapi/chatgpt/"

        self.HEADERS = {
            "apiauth": api_key
        }

    def add_user(self, userToken, expireTime, isPlus):
        url = self.BASE_URL + "user/add"
        data = {
            "userToken": userToken,
            "expireTime": expireTime,  # format: "2024-01-18 00:00:00"
            "isPlus": isPlus  # format: 0,1
        }

        response = requests.post(url, headers=self.HEADERS, data=json.dumps(data))
        # Response: {'code': 1000, 'message': 'BaseResMessage', 'data': {'id': 9}}

        if response.status_code == 200:
            print("Request successful.")
            print("Response:", response.json())
        else:
            print("Request failed.")
            print("Status Code:", response.status_code)
            print("Response:", response.text)

    def delete_user(self, userID):
        url = self.BASE_URL + "user/delete"
        data = {"ids": userID}

        response = requests.post(url, headers=self.HEADERS, data=json.dumps(data))
        # Response: {'code': 1000, 'message': 'BaseResMessage', 'data': {'Locker': {}}}

        if response.status_code == 200:
            print("Request successful.")
            print("Response:", response.json())
        else:
            print("Request failed.")
            print("Status Code:", response.status_code)
            print("Response:", response.text)

    def user_info(self, userID):
        url = self.BASE_URL + "user/info"
        data = {"id": userID}
        response = requests.get(url, headers=self.HEADERS, data=data)
        # Response: {'code': 1000, 'message': 'BaseResMessage', 'data': {'createTime': '2024-01-16 11:08:41', 'deleted_at': None, 'expireTime': '2024-01-20 00:00:00', 'id': 2, 'isPlus': 1, 'remark': 'vip user 1', 'updateTime': '2024-01-17 10:27:34', 'userToken': 'vip1'}}
        if response.status_code == 200:
            print("Request successful.")
            print("Response:", response.json())
        else:
            print("Request failed.")
            print("Status Code:", response.status_code)
            print("Response:", response.text)

    def user_list(self, num):
        url = self.BASE_URL + "user/list"
        data = {"id": num}
        response = requests.post(url, headers=self.HEADERS, data=data)
        # Response: {'code': 1000, 'message': 'BaseResMessage', 'data': [{'createTime': '2024-01-16 11:08:41', 'deleted_at': None, 'expireTime': '2024-01-20 00:00:00', 'id': 2, 'isPlus': 1, 'remark': 'vip user 1', 'updateTime': '2024-01-17 10:27:34', 'userToken': 'vip1'}, {'createTime': '2024-01-17 13:43:03', 'deleted_at': None, 'expireTime': '2024-02-01 00:00:00', 'id': 10, 'isPlus': 0, 'remark': None, 'updateTime': '2024-01-17 13:43:03', 'userToken': 'testtoken2'}, {'createTime': '2024-01-17 13:43:17', 'deleted_at': None, 'expireTime': '2024-04-16 13:43:08', 'id': 11, 'isPlus': 1, 'remark': None, 'updateTime': '2024-01-17 13:43:17', 'userToken': 'testtoken105'}, {'createTime': '2024-01-17 13:43:31', 'deleted_at': None, 'expireTime': '2024-07-15 13:43:25', 'id': 12, 'isPlus': 1, 'remark': None, 'updateTime': '2024-01-17 13:43:31', 'userToken': 'testtoken809'}]}
        if response.status_code == 200:
            print("Request successful.")
            print("Response:", response.json())
        else:
            print("Request failed.")
            print("Status Code:", response.status_code)
            print("Response:", response.text)

    def user_page(self, page, size):
        url = self.BASE_URL + "user/page"
        data = {
            "page": page,
            "size": size
        }
        response = requests.post(url, headers=self.HEADERS, data=data)
        # Response: {'code': 1000, 'message': 'BaseResMessage', 'data': {'list': [{'createTime': '2024-01-16 11:08:41', 'deleted_at': None, 'expireTime': '2024-01-20 00:00:00', 'id': 2, 'isPlus': 1, 'remark': 'vip user 1', 'updateTime': '2024-01-17 10:27:34', 'userToken': 'vip1'}, {'createTime': '2024-01-17 13:43:03', 'deleted_at': None, 'expireTime': '2024-02-01 00:00:00', 'id': 10, 'isPlus': 0, 'remark': None, 'updateTime': '2024-01-17 13:43:03', 'userToken': 'testtoken2'}], 'pagination': {'page': 1, 'size': 2, 'total': 4}}}
        if response.status_code == 200:
            print("Request successful.")
            print("Response:", response.json())
        else:
            print("Request failed.")
            print("Status Code:", response.status_code)
            print("Response:", response.text)

    def user_update(self, createTime, expireTime, id, isPlus, remark, updateTime, userToken):
        url = self.BASE_URL + "user/update"
        data = {
            "createTime": createTime,
            "deleted_at": None,
            "expireTime": expireTime,
            "id": id,
            "isPlus": isPlus,
            "remark": remark,
            "updateTime": updateTime,
            "userToken": userToken
        }
        response = requests.post(url, headers=self.HEADERS, data=data)
        # Response: {'code': 1000, 'message': 'BaseResMessage'}
        if response.status_code == 200:
            print("Request successful.")
            print("Response:", response.json())
        else:
            print("Request failed.")
            print("Status Code:", response.status_code)
            print("Response:", response.text)

# add_user("useradmin2", "2024-01-18 00:00:00", 1)
# delete_user([7,8,9])
# user_info(2)
# user_list(9)
# user_page(1,2)
# user_update(createTime=None, expireTime="2024-01-20 00:00:00", id=2, isPlus=1, remark="vip user 1", updateTime=None, userToken="vip1")
# session部分和user都差不多的，自己写吧，我没有调api加session的需求
