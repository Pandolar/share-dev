# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : main.py
# @Time : 2024/1/18 18:24
# -------------------------------
import uvicorn
from config import CONFIG
from src.app import app
from src.tasks import GoTasks
if __name__ == "__main__":
    # 启动定时任务
    # GoTasks()
    # 启动fastapi
    uvicorn.run(app, host="0.0.0.0", port=CONFIG["PORT"])