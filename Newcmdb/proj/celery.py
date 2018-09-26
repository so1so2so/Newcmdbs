#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('tasks',broker='redis://127.0.0.1/2',backend='redis://127.0.0.1/2',
             include=['proj.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()