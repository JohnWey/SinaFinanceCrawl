#-*- coding: utf-8 -*-

import tushare as ts

#data = ts.get_industry_classified()
#data.to_csv('C:\\Users\\admin\\Downloads\\Code\\WorkSpace\\Python\\SinaFinanceCrawl\\output\\StockBasicInfo.csv')

from sqlalchemy import create_engine
import tushare as ts
import os, sys

df = ts.get_stock_basics()
engine = create_engine('mysql://root:root@127.0.0.1/financedb?charset=utf8')

#存入数据库

reload(sys)
sys.setdefaultencoding('utf-8')

df.to_sql('stock_basics',engine,if_exists='append')

#追加数据到现有表
#df.to_sql('tick_data',engine,if_exists='append')