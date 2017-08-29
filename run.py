#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web

import traceback
from concurrent.futures import ThreadPoolExecutor
from functools import partial


# 多线程执行
EXECUTOR = ThreadPoolExecutor(max_workers=10)


# 数据服务基类,其他服务均继承自此类
# 封装子接口公用的方法
class BaseSearch(tornado.web.RequestHandler):


    @tornado.web.asynchronous
    def asynchronous_get(self, default=None):
        """异步请求，子类在get方法中调用此方法，然后实现_get(self)方法
        """
        def callback(future):
            ex = future.exception()
            print("ex:")
            if ex is None:
                # self.write_result(future.result())
                # print(future.result())

                self.write_result(future.result())
            self.finish()

        return_future = EXECUTOR.submit(self.nomalization_get)
        return_future.add_done_callback(
            lambda future: tornado.ioloop.IOLoop.instance().add_callback(
                partial(callback, future)))

    def nomalization_get(self):

            return self._get()


    def get_argument(self, name, default='', **kwargs):

        value = super(BaseSearch, self).get_argument(name,default)
        return value

    # write result to reaponse
    def write_result(self,result):

        self.write(result)



class PrescriptionTemplate(BaseSearch):

    core = 'prescription_template'
    sort_dict = {
        'default': 'type asc,score desc,template_id asc'
    }

    def get(self):
        self.asynchronous_get()

    def _get(self):

        user = self.get_argument('user', None)
        print("hello")
        # import time
        # time.sleep(0.5)

        # return self.write_result
        return "hello"


application = tornado.web.Application([
    (r"/index", PrescriptionTemplate),
])
if __name__ == "__main__":
    application.listen(8889)
    tornado.ioloop.IOLoop.instance().start()
