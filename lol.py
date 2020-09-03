#!/usr/bin/env python
#encoding: utf-8
 
from subprocess import Popen, PIPE
import os,sys
from commands import getoutput 

class Process(object):

    def __init__(self,proce):
        self.proce = proce

    def getProgPids(self,prog):
        p = Popen(['pidof', prog], stdout=PIPE, stderr=PIPE)
        pids = p.stdout.read().split()
        return pids
 
    def getMemByPid(self,pid):
        fn = os.path.join('/proc', pid, 'status')
        with open(fn) as fd:
            for line in fd:
                if line.startswith('VmRSS'):
                    mem = int(line.split()[1])
                    break
        return mem
 
    def getHttpdMem(self):
        httpd_mem_sum = 0
        pids = obj.getProgPids('%s' % self.proce)
        for pid in pids:
            httpd_mem_sum += obj.getMemByPid(pid)
 
        return httpd_mem_sum
 
 
    def getOsTotalMemory(self):
     
        with open('/proc/meminfo') as fd:
            for line in fd:
                if line.startswith('MemTotal'):
                    total_mem = int(line.split()[1])
                    break
        return total_mem
 
 
    def info(self):
        http_mem  =  obj.getHttpdMem()
        total_mem =  obj.getOsTotalMemory()
        scale = http_mem / float(total_mem) * 100
        #if scale > float(10):
        print '进程%s，Percent: %.2f%%' % (self.proce,scale)

#ret = getoutput("ps -U root -u root -N | awk '{print $4}' | uniq | sort ")
#ret = getoutput("ps aux | sort -k4nr | head -n 100 | awk '{print $11}' | sort -u")
#met = ret.split('\n')
#for i in met:
#    obj = Process(i)
#    obj.info()
#def Cpu_issue():
#        info = getoutput("ps aux | sort -k3nr | head -n 10 | awk '{print $11}' | sort -u")
#        print("占用cpu进程:%s" % info)
#Cpu_issue()
import ping 
result = ping.quiet_ping(sys.argv[1], timeout=2, count=10, psize=64)
print sys.argv[0]
