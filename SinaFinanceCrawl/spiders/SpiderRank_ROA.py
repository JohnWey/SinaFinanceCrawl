#-*- coding: utf-8 -*-
#Autor Zhang Wei

import sys
import time
import ConfigParser
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http.request import Request

day = time.strftime('%Y%m%d',time.localtime(time.time()))



#读取配置文件获取股票代码等信息
conf = ConfigParser.ConfigParser()
conf.read('Stock.conf')
path_profit = conf.get('Stock', 'path_outputfile').replace('?filename','Rank_ROA')

reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = open(path_profit + '.txt', 'w')

#urls = "http://www.caiku.com/ranking/?financeTab/?stockType/1/?page.html"



class SpiderRank(Spider):
    name = "rank_roa"
    allowed_domains = []

    #financeTab = [ '1','3','4','5','6','7','8','9' ]

    #start_urls = [urls.replace('?financeTab', ii.__str__()).replace('?stockType', financeTab[jj]).replace('?page', '1')
    #              for ii in range(11, 19) for jj in range(0, len(financeTab))]

    #start_urls = [urls.replace('?financeTab', '11').replace('?stockType', financeTab[jj]).replace('?page', '1')
                  #for jj in range(0, len(financeTab))]

    #print start_urls
    start_urls = ["http://www.caiku.com/ranking/18/1/1/1.html",
                  "http://www.caiku.com/ranking/18/5/1/1.html",
                  "http://www.caiku.com/ranking/18/6/1/1.html",
                  "http://www.caiku.com/ranking/18/7/1/1.html"
                  ]
    v_itemSet = []

    def parse(self,response):

        sel = Selector(response)
        #sel.remove_namespaces()


        #print response

        #Get the Report Lines, Different Lines means different Report details

        #v_linecnt = sel.xpath('count(//table[@class="tab01 rnk_li w100"]/tbody/tr/td[3]').extract()[0]
        #这个地方不能加tbody,因为tboday是浏览器自己加的，巨坑，
        # 详见：http://stackoverflow.com/questions/30218818/scrapy-returning-a-null-output-when-extracting-an-element-from-a-table-using-xpa

        v_linecnt = sel.xpath('count(//table[@class="tab01 rnk_li w100"]/tr/td[2])').extract()[0]
        v_update_dt = sel.xpath('//*[@id="wrapper"]/div[1]/div[2]/div[4]/div/p/span[1]/text()').extract()[0]

        #print v_update_dt
        #print v_linecnt

        v_onerow = ''

        #Get the Report data
        v_linecnt_int = int(float(v_linecnt.encode("ascii","ignore")))

        for v_rowid in range(2,v_linecnt_int+2):
            for v_col_index in range(2,5):
                v_url = "//table[@class='tab01 rnk_li w100']/tr["+str(v_rowid)+"]/td["+str(v_col_index)+"]//text()"
                tmp = sel.xpath(v_url).extract()[0]

                #print tmp

                if v_onerow<>'':
                    v_onerow = v_onerow+','+tmp
                else:
                    v_onerow = tmp

            print 'roa,'+v_onerow.replace('---',0.0)

            #self.v_itemSet.append(v_onerow)
            v_onerow = ''


        #爬取下一页
        urls = sel.xpath('(//a[@class="navi next_able fr"]/@href)[1]').extract()
        for url in urls:
            #print url
            yield Request(url, callback=self.parse)





# 插入数据到Mysql

# 运行 scrapy runspider < spider_file.py >