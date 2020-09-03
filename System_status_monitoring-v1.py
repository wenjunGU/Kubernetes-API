#!/usr/bin/env python
#coding:utf8

'''
2018-01-19
1、脚本执行环境需CentOS/Ubuntu系统，python版本为2.X
2、执行后会打印出系统版本，python版本，系统异常连接IP，系统超时连接数，系统负载值，系统IO负载值并做相应判断
3、执行后会检测系统CPU以及内存使用率，超过一定阈值将会打印出占用CPU或占用内存前5的进程名称
4、使用方法：python System_status_monitoring-v1.py，直接执行
'''

try:
    from commands import *
    HAS_SSLCONTEXT = True
except ImportError:
    HAS_SSLCONTEXT = False
import re
from subprocess import Popen, PIPE
import os,sys

class bcolors:
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'

        def disable(self):
            self.OKGREEN = ''
            self.WARNING = ''
            self.FAIL = ''
            self.ENDC = ''

class Sys_info(object):

    def Sys(self):
        info = getoutput("lsb_release -i | awk '{print $3}'")
        print(bcolors.OKGREEN + '当前操作系统为:{0}'.format(info) + bcolors.ENDC)
        return info

    def Version(self):
        info = getoutput("python --version")
        print(bcolors.OKGREEN + '当前Py版本为:{0}'.format(info) + bcolors.ENDC)

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
        pids = proces.getProgPids('%s' % self.proce)
        for pid in pids:
            httpd_mem_sum += proces.getMemByPid(pid)
 
        return httpd_mem_sum
 
    def getOsTotalMemory(self):
     
        with open('/proc/meminfo') as fd:
            for line in fd:
                if line.startswith('MemTotal'):
                    total_mem = int(line.split()[1])
                    break
        return total_mem
 
    def info(self):
        http_mem  =  proces.getHttpdMem()
        total_mem =  proces.getOsTotalMemory()
        scale = http_mem / float(total_mem) * 100
        if scale > float(10):
            print(bcolors.FAIL + '占用内存进程%s，Percent: %.2f%%' % (self.proce,scale) + bcolors.ENDC)

class Monitor(object):

    def get_network(self):
        try:  
            import ping
            result = ping.quiet_ping('114.114.114.114', timeout=2, count=10, psize=64)  
            if int(result[0]) == 100:  
                print(bcolors.FAIL + 'Critical - 宕机, To 114.114.114.114 丢包率:%s%%' % (result[0]) + bcolors.ENDC)  
            else:  
                max_time = round(result[1], 2)  
                if int(result[0]) < int(50) and int(result[1]) < int(100):  
                    print(bcolors.OKGREEN + 'OK - To 114.114.114.114 丢包率:%s%%, 最大响应时间:%s ms' % (result[0],max_time) + bcolors.ENDC)  
                elif int(result[0]) >= int(50) or int(result[1]) >= int(100):  
                    print(bcolors.WARNING + 'Warning - To 114.114.114.114 丢包率:%s%%, 最大响应时间:%s ms' % (result[0], max_time) + bcolors.ENDC)
                else:  
                    print(bcolors.FAIL + 'Unknown' + bcolors.ENDC)  
        except IndexError,e:
            print(bcolors.FAIL + e + bcolors.ENDC)

    def get_login(self):
        ips = getoutput("netstat -an | awk '{print $5}' | egrep -Ev '0.0.0.0*|127.0.0.1*'")
        all_ips = re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",ips)
        print(bcolors.OKGREEN + "当前系统最多连接IP:{0}".format(list(set(all_ips))) + bcolors.ENDC)

    def get_Cpu_load(self):
        load = getoutput("iostat -x | awk 'NR==4{print $1}'")
        if load < str(80):
            print(bcolors.OKGREEN + '当前CPU使用率正常:{0}%'.format(load) + bcolors.ENDC)
        else:
            print(bcolors.FAIL + '当前CPU使用率过高:{0}%,cpu占用进程如下'.format(load) + bcolors.ENDC)
            objs.Cpu_issue()

    def Cpu_issue(self):
        info = getoutput("ps aux | sort -k3nr | head -n 5 | awk '{print $11}' | sort -u | sort")
        print(bcolors.FAIL + info + bcolors.ENDC)

    def get_Sys_load(self):
        load = getoutput("uptime | awk '{print $11}'")
        load = load.replace(',','')
        value = getoutput("iostat -x | awk 'NR==1{print $6}'")
        value = re.findall(r"\d+\.?\d*",value)
        for i in value:
            ret = int(i) * float(0.8)
        if load < str(ret):
            print(bcolors.OKGREEN + '当前系统负载正常:{0}'.format(load) + bcolors.ENDC)
        else:
            print(bcolors.FAIL + '当前系统负载过高:{0},请执行 top'.format(load) + bcolors.ENDC)

    def get_Memory(self):
        mem_total = getoutput("free -m | awk 'NR==2{print $2}'")
        mem_used = int(getoutput("free -m | awk 'NR==2{print $3}'"))
        usage = float(mem_used) / float(mem_total) * int(100)
        if usage < float(80):
            print(bcolors.OKGREEN + "当前内存使用率正常:%.2f%%" % usage + bcolors.ENDC)
        else:
            print(bcolors.FAIL + "当前内存使用率过高:%.2f%%" % usage + bcolors.ENDC)
        return usage

    def proceser(self):
        ret = getoutput("ps aux | sort -k4nr | head -n 100 | awk '{print $11}' | sort -u | sort")
        ret = ret.split('\n')
        return ret

    def get_Diskio(self):
        info = getoutput("iostat -x | awk 'NR==7{print $14}'")
        if info < str(80):
                print(bcolors.OKGREEN + "磁盘IO负载正常:{0}%".format(info) + bcolors.ENDC)
        else:
                print(bcolors.FAIL + "磁盘IO读写过高:{0}%,请执行 iostat".format(info) + bcolors.ENDC)

    def run(self):
        ret = getoutput("python -c 'import ping'")
        if ret == '':
            objs.get_network()
        else:
            os.system("easy_install ping")
            objs.get_network()
        objs.get_login()
        objs.get_wait()
        objs.get_Sys_load()
        objs.get_Diskio()
        objs.get_Cpu_load()
 
    def get_wait(self):
        info = getoutput("""netstat -an | grep "TIME_WAIT" | wc -l""")
        if info < str(50):
            print(bcolors.OKGREEN + "系统超时连接数正常:{0}".format(info) + bcolors.ENDC)
        else:
            print(bcolors.FAIL + "系统超时连接数异常:{0},请执行 netstat -an | grep 'TIME_WAIT'".format(info) + bcolors.ENDC)


if __name__ == '__main__':
    obj = Sys_info()
    objs = Monitor()
    try:
        if obj.Sys() == 'CentOS' or obj.Sys() == 'Ubuntu':
            obj.Version()
            objs.run()
            if objs.get_Memory() > float(80):
                for i in objs.proceser():
                    proces = Process(i)
                    proces.info()
        else:
            print(bcolors.WARNING + "System maladjustment!" + bcolors.ENDC)
    except Exception,e:
        print(e)
