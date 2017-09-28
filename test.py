#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
# ret = requests.get("http://127.0.0.1:8002/index?a=1", )
ret = requests.get("http://127.0.0.1:8888/index?a=1", )
print(ret.text)