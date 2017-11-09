#-*- coding: utf-8 -*-


import tushare as ts
import os, sys
import datetime
import time
import pandas as pd

#获取近1个月的数据
end_day = time.strftime('%Y-%m-%d',time.localtime(time.time()))

#print end_day

start_day = datetime.datetime.now() + datetime.timedelta(days=-30)
start_day = start_day.strftime('%Y-%m-%d')





#print start_day
df = ts.get_k_data('510300',start_day,end_day)
r = pd.DataFrame({'1. date':df.date,
                  '2. open':df.open,
                  '3. close':df.close,
                  '4. percent': (df.close-df.open)/df.open*100,
                  '5. code':df.code
                  })


#print r

writer = pd.ExcelWriter('C:/Users/admin/Downloads/Asset/28record.xlsx')

r.to_excel(writer,'510300',index=False)


df = ts.get_k_data('510500',start_day,end_day)
r = pd.DataFrame({'1. date':df.date,
                  '2. open':df.open,
                  '3. close':df.close,
                  '4. percent': (df.close-df.open)/df.open*100,
                  '5. code':df.code
                  })

r.to_excel(writer,'510500',index=False)
