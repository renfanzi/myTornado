#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from controllers.home_handlers import BaseHandler
from tornado.web import RequestHandler
from common.base import result, MyGuid, my_datetime, Config, my_log
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor



class myTest(BaseHandler):
    executor = ThreadPoolExecutor(2)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        self.asynchronous_get()

    def _get(self):

        user = self.get_argument('user', None)
        print("get", user)
        ret = json.dumps(result(status=2000, value="hello world!"))
        return ret

    def post(self, *args, **kwargs):
        self.asynchronous_post()

    def _post(self):
        user = self.get_argument('user', None)
        print("post", user)
        ret = json.dumps(result(status=2000, value="hello world!"))
        return ret