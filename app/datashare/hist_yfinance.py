'''
Author: kevin.z.y kevin.cn.zhengyang@gmail.com
Date: 2025-06-11 18:55:21
LastEditors: kevin.z.y kevin.cn.zhengyang@gmail.com
LastEditTime: 2025-06-11 22:07:31
FilePath: /IntelligenceAgent/app/datashare/hist_yfinance.py
Description: 
Copyright (c) 2025 by ${git_name_email}, All Rights Reserved.
'''


from fastapi import APIRouter, Depends, HTTPException
from pathlib import Path
from datetime import datetime, time

import calendar as cd
import asyncio as ac
import orjson as oj
import yfinance as yf
import pandas as pd

from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Securities

router = APIRouter()

def format_code(symbol: str) -> str:
    seg = symbol.split('.')
    if len(seg) != 2:
        # US market
        return symbol.upper()
    
    code = seg[0]
    mkt = seg[-1].upper()
    if mkt in ['SS', 'SZ']:
        code = code.rjust(6, '0')
    elif mkt == 'HK':
        code = code.rjust(4, '0')
    else:
        raise ValueError(f"unknow symble {symbol}")
    return f"{code}.{mkt}"

@router.post("/securities/add/{code}", tags=["historical data yfinance"])
async def create_item(code: str, db: Session = Depends(get_db)):
    code = format_code(code)
    
    # create if it not exists
    item = db.query(Securities).filter(Securities.code == code).first()
    if not item:
        fpath = Path(__file__).resolve().parent / 'data_yfinance'
        print("current path", fpath)
        sec = yf.Ticker(code)
        name = sec.info.get('longName')
        if not name:
            raise ValueError(f"No data found for {code}")
        
        # check if trading stop or not
        now = datetime.now().time()
        # for SS, SZ and HK
        if code.split('.')[-1] in ['SS', 'SZ', 'HK']:
            stop_time = time(16, 0, 0)
        else:
            stop_time = time(5, 0, 0)
        is_stopped = now > stop_time
        
        # end of week
        today = datetime.today()
        is_weekend = today.weekday() >= 5
        
        # end of month
        last_day = cd.monthrange(today.year, today.month)[1]
        is_month_end = (today.day == last_day)
        
        # get historical data by yfinance
        for interv, label in [('1d', 'daily'), ('1wk', 'weekly'), ('1mo', 'monthly')]:
            hist = sec.history(period='max', interval=interv)
            if hist.empty:
                raise ValueError(f"No {label} data found for {code}")
            else:
                print(f"{label} data records for {code}: {len(hist)}")
                hist.to_csv(str(fpath / f"{label}_{code}.csv"))
                await ac.sleep(5)   # sleep
        
        # store in db
        item = Securities(code=code, name=name, 
                          info=oj.dumps(sec.info), 
                          attrs='')
        db.add(item)
        db.flush()
        print(f"new securities {code}")
    
    return item

@router.post("/securities/del/{code}", tags=["historical data yfinance"])
def read_item(code: str, db: Session = Depends(get_db)):
    code = format_code(code)
    
    item = db.query(Securities).filter(Securities.code == code).first()
    if item:
        db.delete(item)  # 删除对象
        db.commit()      # 提交事务
    return item

@router.get("/securities/all", tags=["historical data yfinance"])
def read_items(db: Session = Depends(get_db)):
    items = db.query(Securities).all()
    return items

@router.get("/securities/{code}", tags=["historical data yfinance"])
def read_item(code: str, db: Session = Depends(get_db)):
    code = format_code(code)
    
    item = db.query(Securities).filter(Securities.code == code).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.get("/securities/holders/{code}", tags=["financial data yfinance"])
async def get_holders(code: str, db: Session = Depends(get_db)):
    code = format_code(code)
    
    item = db.query(Securities).filter(Securities.code == code).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    fpath = Path(__file__).resolve().parent / 'data_yfinance'
    sec = yf.Ticker(code)
    dt = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # get holders by yfinance
    mh = sec.major_holders
    if mh.empty:
        raise ValueError(f"No major holders found for {code}")
    else:
        print(f"major holders data records for {code}: {len(mh)}")
        mh.to_csv(str(fpath / f"mh_{code}_{dt}.csv"))
        await ac.sleep(5)   # sleep 
   
    ih = sec.institutional_holders
    if ih.empty:
        raise ValueError(f"No institutional holders found for {code}")
    else:
        print(f"institutional holders data records for {code}: {len(ih)}")
        ih.to_csv(str(fpath / f"ih_{code}_{dt}.csv"))
        await ac.sleep(5)   # sleep 
    
    fh = sec.mutualfund_holders
    if fh.empty:
        raise ValueError(f"No mutualfund holders found for {code}")
    else:
        print(f"mutualfund holders data records for {code}: {len(fh)}")
        fh.to_csv(str(fpath / f"fh_{code}_{dt}.csv"))
        await ac.sleep(5)   # sleep 
    return item

@router.get("/securities/finance/{code}", tags=["financial data yfinance"])
async def get_finance(code: str, db: Session = Depends(get_db)):
    code = format_code(code)
    
    item = db.query(Securities).filter(Securities.code == code).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    fpath = Path(__file__).resolve().parent / 'data_yfinance'
    sec = yf.Ticker(code)
    dt = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # get finance by yfinance
    fn = sec.financials
    if fn.empty:
        raise ValueError(f"No financials found for {code}")
    else:
        print(f"financials data records for {code}: {len(fn)}")
        fn.to_csv(str(fpath / f"financials_{code}_{dt}.csv"))
        await ac.sleep(5)   # sleep 
   
    bs = sec.balance_sheet
    if bs.empty:
        raise ValueError(f"No balance sheet found for {code}")
    else:
        print(f"balance sheet data records for {code}: {len(bs)}")
        bs.to_csv(str(fpath / f"balance_{code}_{dt}.csv"))
        await ac.sleep(5)   # sleep 
    
    cf = sec.cashflow
    if cf.empty:
        raise ValueError(f"No cashflow found for {code}")
    else:
        print(f"cashflow data records for {code}: {len(cf)}")
        cf.to_csv(str(fpath / f"cashflow_{code}_{dt}.csv"))
        await ac.sleep(5)   # sleep 
    return item
