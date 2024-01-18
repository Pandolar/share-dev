# python3
# -- coding: utf-8 --
# -------------------------------
# @Author : Terry
# @File : main.py
# @Time : 2024/1/18 18:24
# -------------------------------
import uvicorn
from config import CONFIG
from scr.app import app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=CONFIG["PORT"])