#-*- coding: utf-8 -*-
import ConfigParser
from MySqlTool import *
import time

day = time.strftime('%Y%m%d',time.localtime(time.time()))
conf = ConfigParser.ConfigParser()
conf.read('mysql.conf')
conn = init_db(conf, 'Database')


def load2Mysql(type):
    hdngs = ''
    tabname = ''
    filename = ''


    if type == 'financeIndex':
        hdngs = conf.get('Database', 'hdngs_financeIndex')
        tabname = conf.get('Database', 'tabname_financeIdex')
        filename = conf.get('Database', 'path_readFromFile').replace('?filename', 'FinancialGuideLine')

    elif type == 'balancesheet':
        hdngs = conf.get('Database', 'hdngs_balancesheet')
        tabname = conf.get('Database', 'tabname_balancesheet')

        hdngs_bank = conf.get('Database', 'hdngs_balancesheet_bank')
        tabname_bank = conf.get('Database', 'tabname_balancesheet_bank')

        filename = conf.get('Database', 'path_readFromFile').replace('?filename', 'BalanceSheet')

    elif type == 'cashflow':
        hdngs = conf.get('Database', 'hdngs_cashflow')
        tabname = conf.get('Database', 'tabname_cashflow')

        hdngs_bank = conf.get('Database', 'hdngs_cashflow_bank')
        tabname_bank = conf.get('Database', 'tabname_cashflow_bank')

        filename = conf.get('Database', 'path_readFromFile').replace('?filename', 'CashFlow')

    elif type == 'profit':
        hdngs = conf.get('Database', 'hdngs_profit')
        tabname = conf.get('Database', 'tabname_profit')

        hdngs_bank = conf.get('Database', 'hdngs_profit_bank')
        tabname_bank = conf.get('Database', 'tabname_profit_bank')

        filename = conf.get('Database', 'path_readFromFile').replace('?filename', 'Profit')

    #数据日期
    reportDT_list = ['2016']
    #print filename+reportDT_list[0]
    f = open(filename + reportDT_list[0] + '.txt', 'r', 1)

    for line in f:
        # print line
        cnt = len(line.split(','))

        #一般企业资产负债表
        if cnt==110 or cnt == 87 or cnt==91 or cnt==50:
            insert_demo(conn, tabname, hdngs, line)
        #银行或保险业资产负债表
        elif cnt == 95 or cnt == 148 or cnt == 47:
            insert_demo(conn, tabname_bank, hdngs_bank, line)

        elif line.find('NONE')>=0:
            continue
        else:
            print "==================Exception=================="
            print cnt
            print line
            continue
    close_conn(conn)

if __name__ == '__main__':
    #load2Mysql('balancesheet')
    #load2Mysql('cashflow')
    #load2Mysql('profit')
     load2Mysql('financeIndex')

