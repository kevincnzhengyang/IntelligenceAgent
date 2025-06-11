'''
Author: kevin.z.y kevin.cn.zhengyang@gmail.com
Date: 2025-03-08 15:26:29
LastEditors: kevin.z.y kevin.cn.zhengyang@gmail.com
LastEditTime: 2025-03-08 22:58:00
FilePath: /IntelligenceAgent/app/imbot/imbot_model.py
Description: 
Copyright (c) 2025 by ${git_name_email}, All Rights Reserved.
'''

from pydantic import BaseModel
from datetime import datetime
from typing import Union, Literal
from uuid import UUID

class NotificationIn(BaseModel):
    seq_no: Union[int, str, UUID]
    domain: Literal["Task OK", "Task Fail" "Signal Report", "Important News"]
    text: str

class NotificationOut(BaseModel):
    seq_no: Union[int, str, UUID]
    ok: bool
    timestamp: datetime = None
    code: int = None
    description: str = None
