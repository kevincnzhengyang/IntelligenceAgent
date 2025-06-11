'''
Author: kevin.z.y kevin.cn.zhengyang@gmail.com
Date: 2025-03-08 10:14:58
LastEditors: kevin.z.y kevin.cn.zhengyang@gmail.com
LastEditTime: 2025-03-08 23:05:20
FilePath: /IntelligenceAgent/app/imbot/telegram_bot.py
Description: telegram bot to notify client or receive command
Copyright (c) 2025 by ${git_name_email}, All Rights Reserved.
'''

from fastapi import APIRouter
from dotenv import load_dotenv
from datetime import datetime
import requests
import os

from .imbot_model import NotificationIn, NotificationOut

# load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT = os.getenv("CHAT_ID")

router = APIRouter()

def escape_markdown(text):
    escape_chars = '_[]()~`#+-=|{}.!'
    return ''.join(['\\' + c if c in escape_chars else c for c in text])

@router.post("/notify/telegram", tags=["notify"],
            response_model=NotificationOut,
            response_model_exclude_unset=True)
async def send_md_message(info: NotificationIn):
    if "Task OK" == info.domain:
        text = f"✅后台任务完成\n{escape_markdown(info.text)}"
    elif "Task Fail" == info.domain:
        text = f"❌后台任务失败\n{escape_markdown(info.text)}"
    elif "Signal Report" == info.domain:
        text = f"💰明确交易信号\n{escape_markdown(info.text)}"
    elif "Important News" == info.domain:
        text = f"🔥重大消息简讯\n{escape_markdown(info.text)}"
    else:
        return NotificationOut(seq_no=info.seq_no, ok=False, 
                               code=500,
                               description=f"未知通知类型{info.domain}")
        
    rc = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT, "text": text, "parse_mode": "MarkdownV2"}
    )
    
    if rc.ok:
        return NotificationOut(seq_no=info.seq_no, ok=True, 
                               timestamp=datetime.strptime(rc.headers.get("Date"), 
                                                           "%a, %d %b %Y %H:%M:%S %Z"))
    else:
        return NotificationOut(seq_no=info.seq_no, ok=False, 
                               timestamp=datetime.strptime(rc.headers.get("Date"), 
                                                           "%a, %d %b %Y %H:%M:%S %Z"),
                               code=rc.status_code,
                               description=rc.json().get("description"))
