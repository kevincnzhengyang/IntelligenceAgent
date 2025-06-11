'''
Author: kevin.z.y kevin.cn.zhengyang@gmail.com
Date: 2025-06-11 16:41:29
LastEditors: kevin.z.y kevin.cn.zhengyang@gmail.com
LastEditTime: 2025-06-11 20:20:11
FilePath: /IntelligenceAgent/app/models.py
Description: 
Copyright (c) 2025 by ${git_name_email}, All Rights Reserved.
'''


from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import Column, Integer, String

class Securities(Base):
    __tablename__ = "securities"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True, unique=True)
    name = Column(String)
    info = Column(String)
    attrs = Column(String)
