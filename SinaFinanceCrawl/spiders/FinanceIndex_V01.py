#-*- coding: utf-8 -*-
#Autor Zhang Wei

import os, sys
import time
import ConfigParser
from scrapy.spiders import Spider
from scrapy.selector import Selector


day = time.strftime('%Y%m%d',time.localtime(time.time()))


#读取配置文件获取股票代码等信息
conf = ConfigParser.ConfigParser()
conf.read('Stock.conf')
stockcodes = conf.get('Stock', 'stockcodes')
path_financeIndex = conf.get('Stock', 'path_outputfile').replace('?filename','FinancialGuideLine')
urls = conf.get('Stock','url_link').replace('?type','vFD_FinancialGuideLine')

stockcode_list = [ x.replace("\'","") for x in stockcodes.split(',') ]

#stockcode_list = ['000024','300186']
reportDT_list = ['2016']
sys.stdout=open(path_financeIndex+reportDT_list[0]+'.txt','w')

class FinanceIndex(Spider):
    name = "fglcrawl"
    allowed_domains = []

    start_urls = [urls.replace('?stockcode', str(stockcode_list[ii])).replace('?year', str(reportDT_list[jj]))
                  for ii in range(0, len(stockcode_list)) for jj in range(0, len(reportDT_list))]

    def parse(self, response):
        #reload(sys)
        #sys.setdefaultencoding('utf-8')

        sel = Selector(response)
        v_sepSet = response.url.split("/")
        #print response.url
        stockcode = v_sepSet[7]
        #Get the Report Lines, Different Lines means different Report details
        v_cnt = sel.xpath('count(//table[@id="BalanceSheetNewTable0"]/tbody/tr/td[1])').extract()[0]
        v_itemSet = []
        if v_cnt == "93.0":
            #Get the Report date count, if the Report date is current year, it's different with previous year data.
            v_reportdate = sel.xpath('count(//table[@id="BalanceSheetNewTable0"]/tbody/tr[1]/td)').extract()[0]
            i = int(v_reportdate[0]) #Get the Report date count
            #Get the Report data
            for v_col_index in range(2,i+1):
                v_url = "//table[@id='BalanceSheetNewTable0']/tbody/tr/td["+str(v_col_index)+"]/text()"
                v_itemSet = sel.xpath(v_url).extract()

                print "\'"+stockcode+"\'"+",\'"+v_itemSet[0]+'\','+','.join(v_itemSet[1:]).replace("--","0")
        else:
            print "=======================NONE============================="

        #插入数据到Mysql
        #load2cwzb.py




