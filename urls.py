#!/usr/bin/env python
# -*- coding:utf-8 -*-


from controllers.CreateHandlers import  MyTestHandler


urls = list()

testUrls = [(r'/index', MyTestHandler),]

urls += testUrls

