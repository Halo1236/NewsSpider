#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from selenium import webdriver
from lxml import etree
from lxml.etree import tostring, tostringlist

import MySQLdb
import website
from models import db
from models.topic import Topic
reload(sys)
sys.setdefaultencoding("utf-8")


MAIN_URL = u'http://www.sqc.edu.cn'

NEWS_PATH = u'/article-list-157-s52102500_start-%d.html'


class News_spider(object):
    data = {}
    page = 1
    need_save = True
    item = []

    prefs = {
        'profile.default_content_setting_values': {
            'images': 2
        }
    }

    def __init__(self):
        # self.db = MySQLdb.Connect("127.0.0.1", "root", "diaosi", "sqccms")
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('prefs', self.prefs)
        self.driver = webdriver.Chrome(chrome_options=self.options)

    def start(self):
        # cursor = self.db.cursor()
        # cursor.execute()
        topic = Topic.query.all()
        if topic is None or len(topic) == 0:
            self.crawlall(MAIN_URL + NEWS_PATH)
        else:

            pass

    def crawlall(self, url):
        while True:
            index = (self.page - 1) * 14
            print(url % index)
            self.driver.get(url % index)
            page_datas = self.driver.page_source

            if page_datas is not None:
                if self.crawl_item(page_datas) == 1:
                    self.page += 1
                else:
                    ####todo
                    break

    def closeall(self):
        self.driver.quit()

    def crawl_item(self, datas):
        tree = etree.HTML(datas)
        topic_item_tab = tree.xpath('//div[@id="s52102500_content"]/table/tbody')[0]
        topic_item_td = topic_item_tab.xpath(
            '//tr/td[@style="border-bottom:1px #DEDEDE dashed; vertical-align:middle"]')

        for item in topic_item_td:
            print(etree.tostring(item))
            title = item.xpath('//span/span[@class="link_16"]/a/@href')[0]
            url = item.xpath('/span/span[@class="link_16"]/a/@href')[0]
            publisher_time = item.xpath('/tr/span[@class="link_14"]')[0]
            print(title+url+publisher_time)
        if len(topic_item_td) < 14:
            return 0
        else:
            return 1


if __name__ == '__main__':
    try:
        newspider = News_spider()
        newspider.start()
    except KeyboardInterrupt:
        newspider.closeall()
