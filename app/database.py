'''
Author: kevin.z.y kevin.cn.zhengyang@gmail.com
Date: 2025-06-11 16:35:53
LastEditors: kevin.z.y kevin.cn.zhengyang@gmail.com
LastEditTime: 2025-06-11 16:36:04
FilePath: /IntelligenceAgent/app/database.py
Description: 
Copyright (c) 2025 by ${git_name_email}, All Rights Reserved.
'''


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends

DATABASE_URL = "sqlite:///./agent.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # SQLite多线程支持
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 依赖注入函数，管理数据库会话和事务
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()  # 请求成功时提交事务
    except:
        db.rollback()  # 出错时回滚事务
        raise
    finally:
        db.close()
