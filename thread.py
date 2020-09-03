#!/usr/bin/env python
# --*-- coding:utf-8 --*--

import threadpool
import time


class main(object):

    def __init__(self,alist):
        self.alist = alist

    def test(self,a):
        print("hello {0}".format(a))

    def thread(self):
        start_time = time.time()
        pool = threadpool.ThreadPool(5)
        requests = threadpool.makeRequests(self.test, self.alist)
        [pool.putRequest(req) for req in requests]
        pool.wait()
        print('%d second'% (time.time()-start_time))

if __name__ == "__main__":
   obj = main(['world','zhuyun','heitao','lvan','IBM'])
   obj.thread()
