#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pytz import utc
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.executors.pool import ThreadPoolExecutor
from selenium import webdriver
from lxml import etree
from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler
from lxml.etree import tostring, tostringlist
import re
from website import *
from models import *
import gc


reload(sys)
sys.setdefaultencoding("utf-8")


job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

executors = {
    'default': ThreadPoolExecutor(20),
}

prefs = {
    'profile.default_content_setting_values': {
        'images': 2
    }
}

job_list = []


class Sie_Spider(object):
    data = {
        'base_url': '',
        'site_url': '',
        'belong': '',
        'isnotice': False,
        'tab_xpath': '',
        'td_xpath': '',
        'title_xpath': '',
        'url_xpath': '',
        'time_xpath': '',
        'content_xpath': '',
        'count': 0,
    }

    page = 1
    job_list = []

    def __init__(self):
        # self.db = MySQLdb.Connect("127.0.0.1", "root", "diaosi", "sqccms")
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('prefs', prefs)
        # self.driver = webdriver.Chrome(chrome_options=self.options)
        self.driver = webdriver.PhantomJS()

    # def __del__(self):
    #     self.driver.quit()

    def start(self):
        while True:
            sleep(5)
            all_site = find_all_site()
            if all_site is not None:
                for site in all_site:
                    self.data['base_url'] = site.base_url
                    self.data['site_url'] = site.site_url
                    self.data['belong'] = site.belong
                    self.data['isnotice'] = site.isnotice
                    self.data['tab_xpath'] = site.tab_xpath
                    self.data['td_xpath'] = site.td_xpath
                    self.data['time_xpath'] = site.time_xpath
                    self.data['title_xpath'] = site.title_xpath
                    self.data['content_xpath'] = site.content_xpath
                    self.data['count'] = site.count
                    self.data['url_xpath'] = site.url_xpath
                    print(self.data)
                    self.crawl_sqc_all()

    def crawl_sqc_all(self):
        while True:
            url = self.data['base_url'] + self.data['site_url']
            index = (self.page - 1) * self.data['count']
            print(url % index)
            sleep(1)
            self.driver.get(url % index)
            page_datas = self.driver.page_source
            if page_datas is not None:
                if self.crawl_item(page_datas) == 1:
                    self.page += 1
                else:
                    sleep(3)
                    self.page = 1
                    gc.collect()
                    break

    def closeall(self):
        self.driver.quit()

    def crawl_item(self, datas):
        tree = etree.HTML(datas)
        topic_item_tab = tree.xpath(self.data['tab_xpath'])[0]
        topic_item_td = topic_item_tab.xpath(self.data['td_xpath'])

        for item in topic_item_td:
            print(etree.tostring(item))
            url = item.xpath(self.data['url_xpath'])[0].strip()
            title = item.xpath(self.data['title_xpath'])[0].strip()
            publish_time = item.xpath(self.data['time_xpath'])[0].strip()
            print(title + '\n' + url.encode('utf-8') + '\n' + publish_time)

            if find_by_title(title, self.data['base_url'] + url):
                insert_topic_to_db(title, self.data['base_url'] + url, publish_time, self.data['isnotice'],
                                   self.data['belong'])
                self.crawl_article(self.data['base_url'] + url, title, publish_time)
            else:
                return 0
        if len(topic_item_td) < self.data['count']:
            return 0
        else:
            return 1

    def crawl_article(self, path, title, publish_time):
        print(path)
        self.driver.get(path)
        article_datas = self.driver.page_source

        if article_datas is not None:
            arcticle_tree = etree.HTML(article_datas)
            if self.data['belong'] == 'sie':
                publisher = '信息工程学院'
            elif self.data['belong'] == 'bs':
                publisher = '商学院'
            elif self.data['belong'] == 'fzxy':
                publisher = '法政学院'
            elif self.data['belong'] == 'wlxy':
                publisher = '文理学院'
            elif self.data['belong'] == 'jgxy':
                publisher = '建筑工程学院'
            elif self.data['belong'] == 'wy':
                publisher = '外国语学院'
            elif self.data['belong'] == 'jd':
                publisher = '机电工程学院'
            elif self.data['belong'] == 'art':
                publisher = '艺术与传媒学院'
            elif self.data['belong'] == 'tyb':
                publisher = '体育部'
            else:
                publisher = arcticle_tree.xpath('//div[@id="s83407397_content"]//tr[2]//text()')[0]

            content = arcticle_tree.xpath(self.data['content_xpath'])[3]

            htmlinfo = re.compile('src="')
            html_content = htmlinfo.sub('src="' + self.data['base_url'], etree.tostring(content))
            print(title)
            print(html_content)
            insert_article_to_db(title, publisher, publish_time, html_content, path, path)


if __name__ == '__main__':
    try:
        # scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)
        # scheduler._logger = logger
        # scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        #
        #         scheduler.add_job(qalafafa, 'interval', seconds=5, id=site.site_url + site.belong,
        #                           kwargs={'site': 'ewr', })
        #     scheduler.start()
        news = Sie_Spider()
        news.start()
    except KeyboardInterrupt:
        news.closeall()
