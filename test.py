#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
ret = requests.post("http://127.0.0.1:8002/index")
print(ret.text)