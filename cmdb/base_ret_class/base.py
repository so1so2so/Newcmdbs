#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import json
class Ret_class(object):
    code = 10000
    data = None
    errors = None
    session_key=None

    def json(self):
        return json.dumps(self.__dict__)


# d = Ret_class()
# d.data=1
# d.code=1000
# print  d.json()
# print  type(d.json())
