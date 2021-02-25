#!/usr/bin/env python
# --*-- coding:utf-8 --*--

import time 
from commands import getoutput
import os

filte = "AssertionError|OutOfMemoryError|StackOverflowError|AlreadyBoundException|ClassCastException|ConcurrentModificationException|IllegalArgumentException|IllegalStateException|IndexOutOfBoundsException|JSONException|NullPointerException|SecturityException|UnsupportedOperationException|ClassNotFoundException|CloneNotSupportedException|FileAlreadyExistsException|FileNotFoundException|InterruptedException|IOException|SQLException|TimeoutException|UnknownHostException"

class main(object):

    def __init__(self,lpath="/opt/mnkj/jkx-sso-%s.log" % time.strftime('%Y-%m-%d',time.localtime(time.time())),spath="/tmp/logfile.txt",epath="/home/zyadmin/log/Exception.log"):
        self.lpath = lpath
        self.spath = spath
        self.epath = epath

    def get_logfile(self):
        count=0
        thefile=open(self.lpath)
        while True:
            buffer=thefile.read(1024*8192)
            if not buffer:
                break
            count+=buffer.count('\n')
        thefile.close()
        return count

    def set_number(self):
        if not os.path.exists(self.spath):
            with open(self.spath, 'w') as f:
                f.write(str(obj.get_logfile()))

    def get_numfile(self):
        obj.set_number()
        with open(self.spath, 'r') as f:
            return f.read()

    def set_log(self):
        if os.path.exists(self.lpath):
            if int(obj.get_logfile()) >= int(obj.get_numfile()): 
                number = int(obj.get_logfile()) - int(obj.get_numfile())
                keyword = getoutput("tail -%d %s | egrep '%s' | grep -Ev 'InvalidGrantException'" % (number,self.lpath,filte))
                if keyword == "":
                    print("没有错误产生")
                else:
                    keywords = getoutput("tail -%d %s" % (number+10,self.lpath))
                    with open(self.epath, 'a+') as f:
                        f.write(keywords+'\n')
                    print("错误日志已存入")
                with open(self.spath, 'w') as f:
                    f.write(str(obj.get_logfile()))
            else:
                with open(self.spath, 'w') as f:
                    f.write(str(obj.get_logfile()))
                print("增量日志初始化")
        else:
            print("{0}:日志文件不存在".format(self.lpath))

    def check_pointer(self):
        if not self.get_numfile().strip():
            with open(self.spath, 'w') as f:
                f.write(str(obj.get_logfile()))
            print("pointer为空")
        else:
            self.set_log()

if __name__ == '__main__':
    count = 0
    while (count == 0):
        try:
            obj = main()
            obj.check_pointer()
        except Exception,e:
            print(e)
        time.sleep(2)
