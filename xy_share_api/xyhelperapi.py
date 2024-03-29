# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : xyhelperapi.py
# @Time : 2024/1/18 15:33
# -------------------------------
import requests
import json
from config import CONFIG
from src.log import logger


# 感谢xyhelper的群友 查尔斯
class Xyhelper:
    def __init__(self):

        self.BASE_URL = f"https://{CONFIG['SHARE_HOST']}/adminapi/chatgpt/"
        self.HEADERS = {
            "apiauth": CONFIG['SHARE_KEY'],
            "Content-Type": "application/json"
        }

    # ------------------用户相关------------------
    def add_user(self, userToken, expireTime, isPlus):

        url = self.BASE_URL + "user/add"
        data = {
            "userToken": userToken,
            "expireTime": expireTime,  # format: "2024-01-18 00:00:00"
            "isPlus": isPlus  # format: 0,1
        }

        response = requests.post(url, headers=self.HEADERS, data=json.dumps(data))

        if response.status_code == 200 and response.json()['code'] == 1000:
            logger.info(f"{userToken} 用户添加成功")
            return {"code": True, "data": response.json()}
        else:
            logger.error(f"{userToken} 用户添加失败：{response.text}")
            return {"code": False, "msg": response.text}

    def delete_user(self, userID):
        url = self.BASE_URL + "user/delete"
        data = {"ids": userID}

        response = requests.post(url, headers=self.HEADERS, data=json.dumps(data))
        # Response: {'code': 1000, 'message': 'BaseResMessage', 'data': {'Locker': {}}}

        if response.status_code == 200 and response.json()['code'] == 1000:
            logger.info(f"{userID} 用户删除成功")
            return {"code": True}
        else:
            logger.error(f"{userID} 用户删除失败：{response.text}")
            return {"code": False, "msg": response.text}

    def user_info(self, userID):
        url = self.BASE_URL + "user/info"
        data = {"id": userID}
        response = requests.get(url, headers=self.HEADERS, data=data)
        # Response: {'code': 1000, 'message': 'BaseResMessage', 'data': {'createTime': '2024-01-16 11:08:41', 'deleted_at': None, 'expireTime': '2024-01-20 00:00:00', 'id': 2, 'isPlus': 1, 'remark': 'vip user 1', 'updateTime': '2024-01-17 10:27:34', 'userToken': 'vip1'}}
        if response.status_code == 200 and response.json()['code'] == 1000:
            logger.info(f"{userID} 用户信息获取成功")
            return {"code": True, "data": response.json()}
        else:
            logger.error(f"{userID} 用户信息获取失败：{response.text}")
            return {"code": False, "msg": response.text}

    def user_list(self, num):
        url = self.BASE_URL + "user/list"
        data = {"id": num}
        response = requests.post(url, headers=self.HEADERS, data=data)
        # Response: {'code': 1000, 'message': 'BaseResMessage', 'data': [{'createTime': '2024-01-16 11:08:41', 'deleted_at': None, 'expireTime': '2024-01-20 00:00:00', 'id': 2, 'isPlus': 1, 'remark': 'vip user 1', 'updateTime': '2024-01-17 10:27:34', 'userToken': 'vip1'}, {'createTime': '2024-01-17 13:43:03', 'deleted_at': None, 'expireTime': '2024-02-01 00:00:00', 'id': 10, 'isPlus': 0, 'remark': None, 'updateTime': '2024-01-17 13:43:03', 'userToken': 'testtoken2'}, {'createTime': '2024-01-17 13:43:17', 'deleted_at': None, 'expireTime': '2024-04-16 13:43:08', 'id': 11, 'isPlus': 1, 'remark': None, 'updateTime': '2024-01-17 13:43:17', 'userToken': 'testtoken105'}, {'createTime': '2024-01-17 13:43:31', 'deleted_at': None, 'expireTime': '2024-07-15 13:43:25', 'id': 12, 'isPlus': 1, 'remark': None, 'updateTime': '2024-01-17 13:43:31', 'userToken': 'testtoken809'}]}
        if response.status_code == 200 and response.json()['code'] == 1000:
            logger.info(f"{num} 用户列表获取成功")
            return {"code": True, "data": response.json()}
        else:
            logger.error(f"{num} 用户列表获取失败：{response.text}")
            return {"code": False, "msg": response.text}

    def user_page(self, page, size):
        url = self.BASE_URL + "user/page"
        data = {
            "page": page,
            "size": size
        }
        response = requests.post(url, headers=self.HEADERS, data=data)
        # Response: {'code': 1000, 'message': 'BaseResMessage', 'data': {'list': [{'createTime': '2024-01-16 11:08:41', 'deleted_at': None, 'expireTime': '2024-01-20 00:00:00', 'id': 2, 'isPlus': 1, 'remark': 'vip user 1', 'updateTime': '2024-01-17 10:27:34', 'userToken': 'vip1'}, {'createTime': '2024-01-17 13:43:03', 'deleted_at': None, 'expireTime': '2024-02-01 00:00:00', 'id': 10, 'isPlus': 0, 'remark': None, 'updateTime': '2024-01-17 13:43:03', 'userToken': 'testtoken2'}], 'pagination': {'page': 1, 'size': 2, 'total': 4}}}
        if response.status_code == 200 and response.json()['code'] == 1000:
            print("Request successful.")
            return {"code": True, "data": response.json()}

        else:
            print("Request failed.")
            print("Status Code:", response.status_code)
            print("Response:", response.text)
            return {"code": False, "msg": response.text}

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
        if response.status_code == 200 and response.json()['code'] == 1000:
            logger.info(f"{userToken} 用户信息更新成功")
            return {"code": True}
        else:
            logger.error(f"{userToken} 用户信息更新失败：{response.text}")
            return {"code": False, "msg": response.text}

    # ------------------session车辆相关------------------
    def session_page(self, page=1, size=10000):
        url = self.BASE_URL + "session/page"
        data = {
            "page": page,
            "size": size
        }
        response = requests.post(url, headers=self.HEADERS, data=data)
        if response.status_code == 200 and response.json()['code'] == 1000:
            logger.info(f"session列表获取成功")
            return {"code": True, "data": response.json()}
        else:
            logger.error(f"session列表获取失败：{response.text}")
            return {"code": False, "msg": response.text}

    def session_info(self, id):
        url = self.BASE_URL + "session/info"
        data = {
            "id": id
        }
        response = requests.get(url, headers=self.HEADERS, data=data)
        # 返回示例 {"code":1000,"message":"BaseResMessage","data":{"carID":"6e3","createTime":"2024-01-11 19:43:26","deleted_at":null,"email":"gxrt@tvstar.com","id":19,"isPlus":0,"officialSession":"{\"accessToken\":\"e5ayNOyaWwMKrNLzejoRrWOkJjc3H22nvUOkMqoruw09kpNTQ0Ybb_3WuT49vPC-PhllEG4rbOdgiIB-_0Fe5OMxLntTGlse6tt_OTBqI1f5Q\",\"authProvider\":\"auth0\",\"expires\":\"2024-04-10T12:31:43.156Z\",\"models\":[{\"capabilities\":{},\"description\":\"我们最快的模型，非常适合完成大多数日常任务。\",\"max_tokens\":8191,\"product_features\":{},\"slug\":\"text-davinci-002-render-sha\",\"tags\":[\"gpt3.5\"],\"title\":\"Default (GPT-3.5)\"}],\"refreshCookie\":\"eyJhAIhn06CnP1.vCMzJhIW2WaEZxwuPkVzew\",\"user\":{\"email\":\"gxryfmpdhbacbt@tvstar.com\",\"groups\":[],\"iat\":1704976302,\"id\":\"user-hAfBgGjhcdYkVGZ3yT8HAKr2\",\"idp\":\"auth0\",\"image\":\"https://s.gravatar.com/avatar/a849905c10ba9ae162c58b2a31bd2b41?s=480\\u0026r=pg\\u0026d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fgx.png\",\"intercom_hash\":\"8c93cba7ac581b592c86f4971c27909fa66a721fccf2ba8675714d2b5d01b8d9\",\"mfa\":false,\"name\":\"gxryfmpdhbacbt@tvstar.com\",\"picture\":\"https://s.gravatar.com/avatar/a849905c10ba9ae162c58b2a31bd2b41?s=480\\u0026r=pg\\u0026d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fgx.png\"}}","password":"GuBm","remark":"企业号12","status":1,"updateTime":"2024-01-11 20:31:43"}}
        if response.status_code == 200 and response.json()['code'] == 1000:
            logger.info(f"{id} session信息获取成功")
            return {"code": True, "data": response.json()}
        else:
            logger.error(f"{id} session信息获取失败：{response.text}")
            return {"code": False, "msg": response.text}

    def session_delete(self, id: list):
        url = self.BASE_URL + "session/delete"
        data = {
            "id": id
        }
        response = requests.post(url, headers=self.HEADERS, data=data)
        # Response: {'code': 1000, 'message': 'BaseResMessage'}
        if response.status_code == 200 and response.json()['code'] == 1000:
            logger.info(f"{id} session删除成功")
            return {"code": True}
        else:
            logger.error(f"{id} session删除失败：{response.text}")
            return {"code": False, "msg": response.text}

    def session_add(self, carID, email, isPlus, password, remark, status):
        url = self.BASE_URL + "session/add"

        data = {"carID": carID,
                "email": email,
                "isPlus": isPlus,
                "password": password,
                "remark": remark,
                "status": status
                }
        response = requests.post(url, headers=self.HEADERS, data=data)
        # Response: {'code': 1000, 'message': 'BaseResMessage'}
        if response.status_code == 200 and response.json()['code'] == 1000:
            logger.info(f"{carID} session添加成功")
            return {"code": True}
        else:
            logger.error(f"{carID} session添加失败：{response.text}")
            return {"code": False, "msg": response.text}

    def session_update(self, carID, createTime, email, id, isPlus, officialSession, password, remark, status, updateTime):
        url = self.BASE_URL + "session/update"
        # {"carID":"6em3","email":"gxryfmbacbt@tvstar.com","password":"GuWH5RVWX9=VBm","status":1,"isPlus":0,"officialSession":"xxxx","remark":"企业号12 test","createTime":"2024-01-11 19:43:26","deleted_at":null,"id":19,"updateTime":"2024-01-11 20:31:43"}
        data = {
            "createTime": createTime,
            "email": email,
            "id": id,
            "carID": carID,
            "isPlus": isPlus,
            "officialSession": officialSession,
            "password": password,
            "remark": remark,
            "status": status,
            "updateTime": updateTime
        }
        response = requests.post(url, headers=self.HEADERS, data=data)
        # Response: {'code': 1000, 'message': 'BaseResMessage'}
        if response.status_code == 200 and response.json()['code'] == 1000:
            logger.info(f"{carID} session更新成功")
            return {"code": True}
        else:
            logger.error(f"{carID} session更新失败：{response.text}")
            return {"code": False, "msg": response.text}

    # ------------------其他API------------------
    def get_endpoint(self, carid: str):
        url = f"https://{CONFIG['SHARE_HOST']}/endpoint?carid=" + carid
        # url = self.BASE_URL + "getEndpoint"
        response = requests.get(url, headers=self.HEADERS)
        # Response: {"color":"green","label":"3.5","labelColor":"blue","message":"空闲|推荐","namedLogo":"Cockroach Labs","schemaVersion":1}
        # {"color":"grey","label":"","labelColor":"grey","message":"翻车|不可用","namedLogo":"Cockroach Labs","schemaVersion":1}
        # {"color": "green", "label": "PLUS", "labelColor": "purple", "message": "空闲|推荐", "namedLogo": "Cockroach Labs", "schemaVersion": 1}
        if response.status_code == 200:
            return {"code": True, "data": response.json()}
        else:
            logger.error(f"{carid} 获取endpoint失败：{response.text}")
            return {"code": False, "msg": response.text}

    def get_status(self, carid: str):
        # https://go.foxaigc.com/status?carid=tflsbf3o
        url = f"https://{CONFIG['SHARE_HOST']}/status?carid=" + carid
        response = requests.get(url, headers=self.HEADERS)
        # {"accountReady":true,"clears_in":0,"count":3,"isPlus":true,"team_clears_in":0}
        if response.status_code == 200:
            return {"code": True, "data": response.json()}
        else:
            logger.error(f"{carid} 获取status失败：{response.text}")
            return {"code": False, "msg": response.text}


if __name__ == '__main__':
    xyhelper = Xyhelper()
    # xxx
