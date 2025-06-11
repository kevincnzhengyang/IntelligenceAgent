'''
Author: kevin.z.y kevin.cn.zhengyang@gmail.com
Date: 2025-03-08 10:14:01
LastEditors: kevin.z.y kevin.cn.zhengyang@gmail.com
LastEditTime: 2025-06-11 19:19:15
FilePath: /IntelligenceAgent/app/main.py
Description: 
Copyright (c) 2025 by ${git_name_email}, All Rights Reserved.
'''

from fastapi import FastAPI
from .database import engine
from .models import Base  # ORM模型基类

from .schedule import scheduled_tasks
from .imbot import telegram_bot
from .datashare import hist_yfinance

app = FastAPI()

app.include_router(telegram_bot.router)
app.include_router(hist_yfinance.router)

# events on startup
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    
    # register scheduled tasks
    await scheduled_tasks.schedule_tasks()

@app.get("/")
async def root():
    return {"message": "API Server for Intelligence Agent"}
