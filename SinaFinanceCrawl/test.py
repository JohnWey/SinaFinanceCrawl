#coding:utf-8

import os, sys
import time
import ConfigParser
from scrapy.spiders import Spider
from scrapy.selector import Selector

#读取配置文件获取股票代码等信息
conf = ConfigParser.ConfigParser()
conf.read('Stock.conf')
path_profit = conf.get('Stock', 'path_outputfile').replace('?filename','Rank')


reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = open(path_profit + '.txt', 'w')




class test():
    def fun1(self):
        print 'p'

    def fun2(self):
        self.fun1()

if __name__ == '__main__':
    fun2()