#!/usr/bin/env python
# --*-- coding:utf-8 --*--

'''
1、检测本地环境，根据系统环境执行脚本，第一次需安装fping模块
2、排查远程连接IP以及端口是否放行
3、如IP及端口检测正常则需检查其他原因，否则会给出合理建议的url地址
4、执行方法：python check_login.py ip port，带IP以及端口执行,第一次执行需root权限
'''

import socket
from commands import getoutput
import sys,os

class bcolors:  #打印颜色输出控制类
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'

        def disable(self):
            self.OKGREEN = ''
            self.WARNING = ''
            self.FAIL = ''
            self.ENDC = ''

class main(object):

    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

    def Sys(self):  #查询当前系统版本
        info = getoutput("lsb_release -i | awk '{print $3}'")
        print(bcolors.OKGREEN+'当前操作系统为:{0}'.format(info)+bcolors.ENDC)
        return info

    def check_shell(self): #查询当前系统是否存在fping模块
        info = getoutput("whereis fping")
        return len(info)

    def check_ip(self):  #对目标IP做ping检测，取得返回值
        info = getoutput("fping %s | awk '{print $3}'" % (self.ip))
        if info == 'alive':
            print(bcolors.OKGREEN+"对端IP:{0} connect OK".format(self.ip)+bcolors.ENDC)
        else:
            print(bcolors.FAIL+"对端IP:{0} connect Fail,请查阅https://confluence.jiagouyun.com/pages/viewpage.action?pageId=20517889".format(self.ip)+bcolors.ENDC)
        return info

    def check_port(self): #对目标IP的端口做connect检测，取得返回值
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(1)
        try:
            sk.connect((str(self.ip),int(self.port)))
            print(bcolors.OKGREEN+"对端IP:{0} port {1} connect OK".format(self.ip,self.port)+bcolors.ENDC)
        except Exception:
            print(bcolors.FAIL+"对端IP:{0} port {1} connect Fail,请查阅https://confluence.jiagouyun.com/pages/viewpage.action?pageId=20517889".format(self.ip,self.port)+bcolors.ENDC)
        sk.close()

    def run(self,command):  #对fping模块做执行前检测
        if obj.check_shell() != int(6):
            obj.check_ip()
            obj.check_port()
        else:
            os.system("%s install fping > /dev/null" % command)
            obj.check_ip()
            obj.check_port()

if __name__ == '__main__': #执行体，做系统适配
    obj = main(sys.argv[1],sys.argv[2])
    if obj.Sys() == 'CentOS':
        obj.run('yum')
    elif obj.Sys() == 'Ubuntu':
        obj.run('apt-get')
    else:
        print("System maladjustment!")
