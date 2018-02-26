#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from selenium import webdriver
from lxml import etree
from time import sleep
from lxml.etree import tostring, tostringlist
import re
import MySQLdb
import website
from models import db
from models.topic import Topic
from models import *
from models.article import Article

reload(sys)
sys.setdefaultencoding("utf-8")

MAIN_URL = u'http://sie.sqc.edu.cn/'

NEWS_PATH = u'article-list-3-s84673310_start-%d.html'


class Sie_Spider(object):
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

    # def __del__(self):
    #     self.driver.quit()

    def start(self):
        # cursor = self.db.cursor()
        # cursor.execute()
        self.crawl_sqc_all(MAIN_URL + NEWS_PATH)

    def crawl_sqc_all(self, url):
        while True:
            index = (self.page - 1) * 13
            print(url % index)
            sleep(1)
            self.driver.get(url % index)
            page_datas = self.driver.page_source

            if page_datas is not None:
                if self.crawl_item(page_datas) == 1:
                    self.page += 1
                else:
                    sleep(5)
                    self.page = 1

    def closeall(self):
        self.driver.quit()

    def crawl_item(self, datas):
        tree = etree.HTML(datas)
        topic_item_tab = tree.xpath('//div[@id="s84673310_content"]/table/tbody')[0]
        topic_item_td = topic_item_tab.xpath(
            '//tr/td[@style="border-bottom:1px #dddddd dashed; vertical-align:middle"]')

        for item in topic_item_td:
            print(etree.tostring(item))
            url = item.xpath('span/span[@class="link_14"]/a/@href')[0].strip()
            title = item.xpath('span/span[@class="link_14"]/a/text()')[0].strip()
            publish_time = item.xpath('span[@class="link_13"]/text()')[0].strip()
            print(title + '\n' + url.encode('utf-8') + '\n' + publish_time)

            if find_by_title(title, MAIN_URL + url):
                insert_topic_to_db(title, MAIN_URL + url, publish_time, False, 'sie')
                self.crawl_article(MAIN_URL + url)
            else:
                return 0
        if len(topic_item_td) < 13:
            return 0
        else:
            return 1

    def crawl_article(self, path):
        print(path)
        self.driver.get(path)
        article_datas = self.driver.page_source

        if article_datas is not None:
            arcticle_tree = etree.HTML(article_datas)

            tite = arcticle_tree.xpath('//div[@id="s70184755_content"]//tr[1]//text()')[0]
            publisher = '信息工程学院'
            publish_time = arcticle_tree.xpath(
                '//div[@id="s70184755_content"]//tr[2]//text()')[0]
            content = arcticle_tree.xpath('//div[@id="s70184755_content"]//tr')[3]

            htmlinfo = re.compile('src="')
            html_content = htmlinfo.sub('src="' + MAIN_URL, etree.tostring(content))
            print(tite)
            print(html_content)
            insert_article_to_db(tite, publisher, publish_time, html_content, path, path)


if __name__ == '__main__':
    try:
        newspider = Sie_Spider()
        newspider.start()
        # newspider.crawl_article('http://sie.sqc.edu.cn/article-detail-983518.html')
    except KeyboardInterrupt:
        newspider.closeall()
