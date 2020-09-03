#!/usr/bin/env python
# --*-- coding:utf-8 --*--

'''
1、检测当前服务器挂载磁盘目录总空间大小以及使用率
2、判断磁盘挂载目录使用率，超过%80则打印出所有该目录下占用空间超过磁盘总空间的%2的文件
3：使用方法：python check_disk.py，直接执行
'''

from commands import getoutput
import sys,re

class bcolors:  #打印输出颜色控制类
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

    def __init__(self,disk):
        self.disk = disk

    def Disk_size(self):  #取得磁盘挂载目录总空间大小值
        info = getoutput("df -m | grep '%s' | awk 'NR==1{print $2}'" % self.disk)
        return info

    def Disk_usage(self):  #取得磁盘挂载目录使用率值
        info = getoutput("df -m | grep '%s' | awk 'NR==1{print $5}'" % self.disk)
        info = re.findall(r"\d+\.?\d*",info)
        for i in info:
            return i

    def file_usage(self):  #根据磁盘总空间%2的值找出占用磁盘空间的文件
        info = re.findall(r"\d+\.?\d*", obj.Disk_size())
        for i in info:
            size = float(i) * float(0.01)
        files = getoutput("find %s -xdev -size +%sM" % (self.disk,int(size)))
        files = files.split('\n')
        for i in files:
            ret = getoutput("du -sh %s" % i)
            print(bcolors.WARNING+ret+bcolors.ENDC)


try:  #执行体，遍历系统磁盘挂载目录，判断使用率并给出相应输出
    info = getoutput("df -m | awk '{print $6}' | egrep -Ev 'Mounted|/dev|/sys|/run|/boot'")
    for i in info.split('\n'):
        obj = main(i)
        if obj.Disk_usage() <= str(50):
            print(bcolors.OKGREEN+"磁盘目录<{0}>总空间{1}M,使用率达到{2}%,属正常范围".format(i,obj.Disk_size(),obj.Disk_usage())+bcolors.ENDC)
        else:
            print(bcolors.FAIL+"磁盘目录<{0}>总空间{1}M,使用率达到{2}%,占用磁盘空间大于%2文件如下:".format(i,obj.Disk_size(),obj.Disk_usage())+bcolors.ENDC)
            obj.file_usage()
except Exception as e:
    print(e)
