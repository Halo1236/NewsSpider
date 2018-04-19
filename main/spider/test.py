#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import re
import json

# def my_job1():
#     print('my_job1 is running, Now is %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#
#
# def my_job2():
#     print('my_job2 is running, Now is %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#
#
# sched = BackgroundScheduler(daemon=False)
# # 每隔5秒运行一次my_job1
# sched.add_job(my_job1, 'interval', seconds=5, id='my_job1')
# sched.start()


a = {'1': datetime.now, '2': 2}
list = []
list.append(a)
list.append(a)
# q1 = re.findall(r'(?<=\[).*?(?=])', a)


print(json.dumps(list))
