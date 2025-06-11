'''
Author: kevin.z.y kevin.cn.zhengyang@gmail.com
Date: 2025-06-11 16:23:55
LastEditors: kevin.z.y kevin.cn.zhengyang@gmail.com
LastEditTime: 2025-06-11 19:20:05
FilePath: /IntelligenceAgent/app/schedule/scheduled_tasks.py
Description: 
Copyright (c) 2025 by ${git_name_email}, All Rights Reserved.
'''


from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

scheduler = BackgroundScheduler()


# ---------------------------------
#              tasks
# ---------------------------------
def tick():
    print(f'Tick! The time is: {datetime.now()}')


# ---------------------------------
#      entrance for schedule
# ---------------------------------
async def schedule_tasks():
    scheduler.add_job(tick, 'interval', seconds=30)  # 每3秒执行一次
    
    scheduler.start()
    