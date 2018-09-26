#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from celery import Celery

app = Celery('tasks',broker='redis://127.0.0.1/2',backend='redis://127.0.0.1/2')

@app.task
def add(x,y):
    print("running...",x,y)
    return x+y