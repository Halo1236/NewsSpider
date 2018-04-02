# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient

from bs4 import BeautifulSoup as BS
import urllib
from lxml import etree,html
from lxml.etree import tostring
import sys
import time
import random
import os
import multiprocessing
import json
import datetime

reload(sys)
sys.setdefaultencoding("utf-8")


class priceInformation(object):
    d = {}
    judge = True
    picture_url = ''
    json_data_thisyear = []
    json_data_lastyear = []
    need_second_crawl = False
    need_save = True
    page = 1
    datas = []
    is_crawled = False

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 27017
        self.client = MongoClient(self.host, self.port)
        self.db = self.client['LzScrapy']
        self.collection = self.db['price_information_category_collection']
        self.collection_province = self.db['price_province_collection']
        self.collection_with_province = self.db['price_with_province_collection']
        self.collection_final = self.db['price_final_collection']
        self.collection_price = self.db['price_collection']
        self.collection_price_year = self.db['price_year_collection']
        self.collection_time = self.db['price_time']
        self.options = webdriver.ChromeOptions()
        self.prefs = {
            'profile.default_content_setting_values': {
                'images': 2
            }
        }
        self.options.add_experimental_option('prefs', self.prefs)
        # self.PROXY = ['119.29.103.13:8888','118.178.227.171:80']
        # number = random.randint(0,2)
        # self.options.add_argument('--proxy-server=%s' % self.PROXY[number])
        # self.driver = webdriver.Chrome("C:\Users\sunxufeng\Downloads\chromedriver.exe",chrome_options = self.options)
        # self.driver.implicitly_wait(10)
        # self.driver = webdriver.PhantomJS()

    def start(self, index):
        if self.collection_final.count({'is_crawled': 0}) == 0:
            item_times = self.collection_time.find().limit(1)
            for item_time in item_times:
                now = datetime.datetime.strptime(item_time['endTime'], "%Y-%m-%d")
                date = now + datetime.timedelta(days=1)
                endTime = datetime.datetime.now()
                self.collection_time.update(item_time,
                                            {"$set": {'startTime': str(date)[0:11], 'endTime': str(endTime)[0:11]}})

            items = self.collection_final.find()
            for item in items:
                self.collection_final.update(item, {"$set": {'is_crawled': 0}})
        # items = self.collection_final.find({'product_name':'畜产品','product_name_child':'鸡蛋','product_province':'安徽省','product_province_child':'安徽合肥周谷堆农产品批发市场'})
        items = self.collection_final.find({'is_crawled': 0})
        # if index == 3:
        #     self.options.add_argument('--proxy-server=180.114.93.186:47974')
        # else:
        #     self.PROXY = ['121.237.6.20:8118','219.137.206.66:53281']
        #     self.options.add_argument('--proxy-server=%s' % self.PROXY[index-1])
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.driver.implicitly_wait(10)
        count = 0
        item_times = self.collection_time.find().limit(1)
        startTime = ''
        endTime = ''
        for item_time in item_times:
            startTime = item_time['startTime']
            endTime = item_time['endTime']

        for item in items:
            self.is_crawled = False
            if item['product_province_child'] == '':
                continue
            if item.has_key('is_crawled'):
                if item['is_crawled'] == 1:
                    continue
                else:
                    pass
            self.need_second_crawl = False
            self.page = 1
            self.judge = True
            self.need_save = True
            while self.judge:
                self.startScrapy(index,
                                 'http://nc.mofcom.gov.cn/channel/jghq2017/price_list.shtml?par_craft_index=' + item[
                                     'product_id'] + '&craft_index=' + item[
                                     'product_id_child'] + '&startTime=' + startTime + '&endTime=' + endTime + '&par_p_index=' +
                                 item['product_province_id'] + '&p_index=' + item[
                                     'product_province_id_child'] + '&keyword=&page=' + str(self.page), item)
                self.page += 1
            if self.datas is None or len(self.datas) == 0:
                pass
            else:
                for data in self.datas:
                    # print item['product_province_child']
                    self.collection_price.save(data)
            self.datas = []
            if self.is_crawled:
                # self.collection_final.update(item,{"$set":{'is_crawled':1}})
                self.collection_final.update(item, {"$set": {'is_crawled': 1}})
            # print count
            count += 1
            if count == 100:
                break
        if count == 100:
            self.driver.quit()
            time.sleep(2)
            self.start(3)
            pass
        print 'finish'

    # def start_test(self, index):
    #     # self.startCategory_Product('http://nc.mofcom.gov.cn/channel/gxdj/jghq/jg_list.shtml')
    #
    #     # items = self.collection.find()
    #     # for item in items:
    #     #     self.startCategory_Product_Child('http://nc.mofcom.gov.cn/channel/gxdj/jghq/jg_list.shtml?par_craft_index=' + item['product_id'] + '&craft_index=&startTime=2017-05-07&endTime=2017-08-05&par_p_index=&p_index=&keyword=',item)
    #
    #     # items = self.collection.find().limit(1)
    #     # for item in items:
    #     #     self.startCategory_Province('http://nc.mofcom.gov.cn/channel/gxdj/jghq/jg_list.shtml?par_craft_index=' + item['product_id'] + '&craft_index=' + item['product_id_child']  + '&startTime=2017-05-07&endTime=2017-08-05&par_p_index=&p_index=&keyword=')
    #
    #     # self.add_Province()
    #
    #     items = self.collection_with_province.find(no_cursor_timeout=True).skip((index - 1) * 2534).limit(1)
    #     # items = self.collection_with_province.find(no_cursor_timeout=True)
    #     for item in items:
    #         if item.has_key('is_crawled'):
    #             if item['is_crawled'] == 1:
    #                 pass
    #         else:
    #             self.startFinal('http://nc.mofcom.gov.cn/channel/jghq2017/price_list.shtml?par_craft_index=' + item[
    #                 'product_id'] + '&craft_index=' + item[
    #                                 'product_id_child'] + '&startTime=2017-05-07&endTime=2017-08-29&par_p_index=' +
    #                             item['product_province_id'] + '&p_index=&keyword=&page=' + str(), item)

    def startScrapy(self, index, url, item):
        time.sleep(1)
        self.driver.get(url)
        data = self.driver.page_source
        tree = etree.HTML(data)
        sel_tr_lst = tree.xpath('//table[@class="table-01 mt30"]/tbody/tr')
        sel_table_lst = tree.xpath('//table[@class="table-01 mt30"]')
        if sel_table_lst is None or len(sel_table_lst) == 0:
            print index
        else:
            if sel_tr_lst is None or len(sel_tr_lst) == 1:
                self.is_crawled = True
                self.judge = False
            else:
                for sel_tr in sel_tr_lst:
                    sel_td_lst = sel_tr.xpath('td')
                    self.d = {}
                    if not sel_td_lst is None and len(sel_td_lst) == 5:
                        i = 0
                        for sel_td in sel_td_lst:

                            if i == 0:
                                self.d['product_date'] = sel_td.xpath('text()')[0].replace('\r', '').replace('\n',
                                                                                                             '').strip()
                            elif i == 1:
                                pass
                            elif i == 2:
                                sel_td_span_lst = sel_td.xpath('span/text()')
                                if not sel_td_span_lst is None and len(sel_td_span_lst) > 0:
                                    sel_td_span = sel_td_span_lst[0]
                                    self.d['product_price'] = sel_td_span.replace('\r', '').replace('\n', '').strip()
                            elif i == 3:
                                tem = {'product_date': self.d['product_date'], 'product_price': self.d['product_price'],
                                       'product_province_id_child': item['product_province_id_child'],
                                       'product_province_id': item['product_province_id'],
                                       'product_id_child': item['product_id_child'], 'product_id': item['product_id']}
                                if self.collection_price.count(tem) == 0:
                                    pass
                                else:
                                    self.judge = False
                                    self.need_save = False
                                    break
                                if self.datas is None or len(self.datas) == 0:
                                    pass
                                else:
                                    for data in self.datas:
                                        if data['product_date'] == self.d['product_date']:
                                            self.judge = False
                                            self.need_save = False
                                            break
                            elif i == 4:
                                if self.need_second_crawl:
                                    sel_url_lst = sel_td.xpath('a/@href')
                                    self.url = ''
                                    self.json_data_thisyear = []
                                    self.json_data_lastyear = []
                                    if sel_url_lst is None or len(sel_url_lst) == 0:
                                        pass
                                    else:
                                        tem = {}
                                        url = 'http://nc.mofcom.gov.cn/nc/gxdj/schq/get_date_curve.jsp?var='
                                        sel_url = sel_url_lst[0]
                                        sel_url_1 = sel_url.split('?')[1]
                                        sel_url_2s = sel_url_1.split('&')
                                        for sel_url_2 in sel_url_2s:
                                            sel_url3s = sel_url_2.split('=')
                                            if sel_url3s[0] == 'p_index':
                                                url += sel_url3s[1] + '-'
                                            elif sel_url3s[0] == 'craft_index':
                                                url += sel_url3s[1] + '-'
                                            elif sel_url3s[0] == 'year1':
                                                url += sel_url3s[1] + '-'
                                            elif sel_url3s[0] == 'year2':
                                                url += sel_url3s[1] + '&n='
                                        self.picture_url = url
                                        self.driver.get(url)
                                        data_json = self.driver.page_source
                                        tree_json = etree.HTML(data_json)

                                        json_picture_summary_titlename_lst = tree_json.xpath('//statdatas/@titlename')
                                        if json_picture_summary_titlename_lst is None or len(
                                                json_picture_summary_titlename_lst) == 0:
                                            pass
                                        else:
                                            tem['titlename'] = json_picture_summary_titlename_lst[0]

                                        json_picture_summary_titlesubhead_lst = tree_json.xpath(
                                            '//statdatas/@titlesubhead')
                                        if json_picture_summary_titlesubhead_lst is None or len(
                                                json_picture_summary_titlesubhead_lst) == 0:
                                            pass
                                        else:
                                            tem['titlesubhead'] = json_picture_summary_titlesubhead_lst[0]

                                        json_picture_summary_pricename_lst = tree_json.xpath('//statdatas/@pricename')
                                        if json_picture_summary_pricename_lst is None or len(
                                                json_picture_summary_pricename_lst) == 0:
                                            pass
                                        else:
                                            tem['pricename'] = json_picture_summary_pricename_lst[0]

                                        json_picture_summary_lastyear_lst = tree_json.xpath('//statdatas/@lastyear')
                                        if json_picture_summary_lastyear_lst is None or len(
                                                json_picture_summary_lastyear_lst) == 0:
                                            pass
                                        else:
                                            lastyear = json_picture_summary_lastyear_lst[0]

                                        json_picture_summary_thisyear_lst = tree_json.xpath('//statdatas/@thisyear')
                                        if json_picture_summary_thisyear_lst is None or len(
                                                json_picture_summary_thisyear_lst) == 0:
                                            pass
                                        else:
                                            thisyear = json_picture_summary_thisyear_lst[0]

                                        json_picture_lst = tree_json.xpath('//statdatas/cabinet')
                                        if json_picture_lst is None or len(json_picture_lst) == 0:
                                            pass
                                        else:
                                            k = 0
                                            for json_picture in json_picture_lst:
                                                k += 1
                                                json_obj = {}
                                                lastyear_lst = {}
                                                thisyear_lst = {}
                                                lastprice_lst = json_picture.xpath('lastprice/text()')
                                                if lastprice_lst is None or len(lastprice_lst) == 0:
                                                    pass
                                                else:
                                                    lastyear_lst['price'] = lastprice_lst[0]

                                                thisprice_lst = json_picture.xpath('thisprice/text()')
                                                if thisprice_lst is None or len(thisprice_lst) == 0:
                                                    pass
                                                else:
                                                    thisyear_lst['price'] = thisprice_lst[0]

                                                markettime_lst = json_picture.xpath('markettime/text()')
                                                if markettime_lst is None or len(markettime_lst) == 0:
                                                    pass
                                                else:
                                                    lastyear_lst['markettime'] = markettime_lst[0]
                                                    thisyear_lst['markettime'] = markettime_lst[0]
                                                self.json_data_thisyear.append(thisyear_lst)
                                                self.json_data_lastyear.append(lastyear_lst)
                                        tem['product_id'] = item['product_id']
                                        tem['product_name'] = item['product_name']
                                        tem['product_id_child'] = item['product_id_child']
                                        tem['product_name_child'] = item['product_name_child']
                                        tem['product_province'] = item['product_province']
                                        tem['product_province_id'] = item['product_province_id']
                                        tem['product_province_id_child'] = item['product_province_id_child']
                                        tem['product_province_child'] = item['product_province_child']
                                        # tem['picture_data'] = self.json_data
                                        tem['picture_url'] = self.picture_url
                                        tem[lastyear] = self.json_data_lastyear
                                        tem[thisyear] = self.json_data_thisyear
                                        if self.collection_price_year.count(tem) == 0:
                                            self.collection_price_year.save(tem)
                                        else:
                                            pass
                                        self.need_second_crawl = False
                            i += 1
                            # print json_data
                        if self.need_save:
                            # self.d['picture_data'] = self.json_data
                            # self.d['picture_url'] = self.picture_url
                            self.d['product_id'] = item['product_id']
                            self.d['product_name'] = item['product_name']
                            self.d['product_id_child'] = item['product_id_child']
                            self.d['product_name_child'] = item['product_name_child']
                            self.d['product_province'] = item['product_province']
                            self.d['product_province_id'] = item['product_province_id']
                            self.d['product_province_id_child'] = item['product_province_id_child']
                            self.d['product_province_child'] = item['product_province_child']
                            self.d['is_post'] = 0
                            # self.datas.append(self.d)
                    if self.need_save:
                        if not self.d:
                            pass
                        else:
                            self.datas.append(self.d)
                    self.is_crawled = True
                    # self.collection_price.save(self.d)

    def startCategory_Product(self, url):
        self.driver.get(url)
        # print ' 11111111 ' + self.driver.current_url
        data = self.driver.page_source
        tree = etree.HTML(data)
        content_product = tree.xpath('//div[@class="k_searchBox_01 mt10"]/p/select')[0]
        content_product_lst = content_product.xpath('option')
        i = 0
        print len(content_product_lst)
        for content_product in content_product_lst:
            self.d = {}
            if i == 0:
                pass
            else:
                self.d['product_id'] = content_product.xpath('@value')[0]
                self.d['product_name'] = content_product.xpath('text()')[0]
                self.collection.save(self.d)
            i += 1

    def startCategory_Product_Child(self, url, item):
        self.driver.get(url)
        # print ' 11111111 ' + self.driver.current_url
        data = self.driver.page_source
        tree = etree.HTML(data)
        content_product = tree.xpath('//div[@class="k_searchBox_01 mt10"]/p/select')[1]
        content_product_lst = content_product.xpath('option')
        i = 0
        print len(content_product_lst)
        for content_product in content_product_lst:
            self.d = {}
            if i == 0:
                pass
            else:
                self.d['product_id'] = item['product_id']
                self.d['product_name'] = item['product_name']
                self.d['product_id_child'] = content_product.xpath('@value')[0]
                self.d['product_name_child'] = content_product.xpath('text()')[0]
                self.collection.save(self.d)
                self.collection.remove(item)
            i += 1

    def startCategory_Province(self, url):
        self.driver.get(url)
        # print ' 11111111 ' + self.driver.current_url
        data = self.driver.page_source
        tree = etree.HTML(data)
        content = tree.xpath('//div[@class="k_searchBox_01 mt10"]/p')[1]
        content_product = content.xpath('select')[0]
        content_product_lst = content_product.xpath('option')
        i = 0
        print len(content_product_lst)
        for content_product in content_product_lst:
            self.d = {}
            if i == 0:
                pass
            else:
                self.d['product_province_id'] = content_product.xpath('@value')[0]
                self.d['product_province'] = content_product.xpath('text()')[0]
                self.collection_province.save(self.d)
            i += 1

    def add_Province(self):
        item_products = self.collection.find()
        item_provinces = self.collection_province.find()

        provinces_name = []
        provinces_id = []
        for item_province in item_provinces:
            provinces_name.append(item_province['product_province'])
            provinces_id.append(item_province['product_province_id'])

        print len(provinces_name)
        k = 0
        for item_product in item_products:
            # self.collection.remove(item_product)
            i = 0
            k += 1
            # print k
            for province_name in provinces_name:
                self.d = {}
                self.d['product_id'] = item_product['product_id']
                self.d['product_name'] = item_product['product_name']
                self.d['product_id_child'] = item_product['product_id_child']
                self.d['product_name_child'] = item_product['product_name_child']
                self.d['product_province'] = province_name
                self.d['product_province_id'] = provinces_id[i]
                self.collection_with_province.save(self.d)
                i += 1
                # print 'i + ' + str(i)

    def startFinal(self, url, item):
        # print url
        # time.sleep(random.randint(1,5))
        time.sleep(1)
        self.driver.get(url)
        data = self.driver.page_source
        tree = etree.HTML(data)
        content_temp = tree.xpath('//div[@class="k_searchBox_01 mt10"]/p')
        if content_temp is None or len(content_temp) == 0:
            pass
        else:
            content = content_temp[1]
            content_product = content.xpath('select')[1]
            content_product_lst = content_product.xpath('option')
            i = 0
            for content_product in content_product_lst:
                self.d = {}
                if i == 0:
                    self.collection_with_province.update(item, {"$set": {'is_crawled': 1}})
                    pass
                else:
                    self.d['product_id'] = item['product_id']
                    self.d['product_name'] = item['product_name']
                    self.d['product_id_child'] = item['product_id_child']
                    self.d['product_name_child'] = item['product_name_child']
                    self.d['product_province'] = item['product_province']
                    self.d['product_province_id'] = item['product_province_id']
                    self.d['product_province_id_child'] = content_product.xpath('@value')[0]
                    self.d['product_province_child'] = content_product.xpath('text()')[0]
                    self.collection_final.save(self.d)
                    # self.collection_with_province.update(item,{"$set":{'is_crawled':1}})
                i += 1


def start_price(index):
    priceInformation().start(index)


def start_multi_thread():
    pool = multiprocessing.Pool(processes=5)
    index = 0
    for cfg in range(1, 4):
        index += 1
        pool.apply_async(start_price, (index,))
    pool.close()
    pool.join()


if __name__ == '__main__':
    # start_multi_thread()
    priceInformation().start(3)
