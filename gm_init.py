#!/usr/bin/env python
# --*-- coding:utf-8 --*--

import subprocess
import os,sys,time
import socket,fcntl,struct
from commands import getoutput
from optparse import OptionParser
import re

'''
time:2019-11-12
user:wenjun.gu
role:game-server系统环境初始化
project:NXX

##保证在root环境下执行，会较为大量调用系统shell
'''

class init_os(object):

    def __init__(self,user="admin",ethname="eth0",path="/etc/gm-init"):
        self.user = user
        self.ethname = ethname
        self.path = path

    def exec_run(self,cmd):
        stdoutls = []
        def receive():
            (stdout) = \
                proc.communicate()
        try:
            for rcmd in cmd:
                proc =subprocess.Popen(rcmd,
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE)
                while proc.returncode is None:
                    stdout = proc.communicate()
                stdoutls.append(stdout)
        except Exception,e:
           print e
           sys.exit(0)
        finally:
           return stdoutls

    def Sys(self):
        sys_info = getoutput("lsb_release -i | awk '{print $3}'")
        return sys_info

    def Init_sys(self):
        try:
            self.exec_run(["echo 'ulimit -c unlimited' >> /etc/profile","echo 'ulimit -SHn 65536' >> /etc/profile","source /etc/profile","yum -y install mysql redis gcc gcc-c++"])
        except Exception,e:
            print(e)

    def getip(self,ethname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', ethname[:15]))[20:24])
        return ip

    def Set_hostname(self):
        raw = raw_input("pls input hostname:")
        if raw != "":
            os.system("hostnamectl set-hostname {0}".format(raw))
            self.exec_run(["echo {0} > /etc/hostname".format(raw)])
            print("The hostname setting end")
        else:
            print("not input hostname")
            sys.exit()

    def Mount_disk(self):
        disk_info = getoutput("df | grep '/dev/vdb'")
        if disk_info == "":
                os.mkdir("/home/nxx")
                self.exec_run(["mkfs.ext4 /dev/vdb","echo '/dev/vdb                                  /home/nxx               ext4    defaults        0 0' >> /etc/fstab","mount -a"])
                print("Disk Initialize end")
        else:
            print("Disk already Initialize")

    def check_port(self):
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(1)
        try:
            sk.connect((str(self.getip("eth0")),int(58422)))
            return "OK"
        except Exception:
            return "FAIL"
            sk.close()

    def Change_ssh(self):
        if self.check_port() != "FAIL":
            print("ssh port already is 58422")
        else:
            self.exec_run(["sed -i 's@#Port 22@Port 58422@g' /etc/ssh/sshd_config","systemctl restart sshd"])
            print("The ssh-port setting end")

    def Check_openssl(self):
        info = getoutput("openssl version | awk {'print $2'}")
        if info == "1.0.2k-fips":
            print("openssl version is OK")
        else:
           self.exec_run(["yum makecache","yum update openssl"])
           print("The openssl-version update end")

    def Add_user(self):
        info = getoutput("cat /etc/passwd | grep '^{0}:' -c".format(self.user))
        if info != "1":
            self.exec_run(["useradd {0}".format(self.user),"echo 'jjker@1314' | passwd {0} --stdin".format(self.user),"echo 'admin ALL=(ALL) NOPASSWD: /usr/bin/su' >> /etc/sudoers"])
            print("The gm-user add end")
        else:
            print("gm-user already existing")

    def Install_salt(self):
        if os.path.exists("/etc/salt"):
            print("salt-minion already install")
        else:
            name = getoutput("hostname")
            self.exec_run(["wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo","yum install salt-minion -y","echo 'master: 47.103.107.5' > /etc/salt/minion","echo 'id: {0}' >> /etc/salt/minion".format(name),"systemctl enable salt-minion","systemctl start salt-minion"])
            print("install salt-minion end")

    def Init_all(self):
        if os.path.exists(self.path):
            print("OS already Initialize Off")
            sys.exit()
        else:
            os.mkdir(self.path)
            self.Set_hostname()
            self.Change_ssh()
            self.Check_openssl()
            self.Add_user()
            self.Mount_disk()
            self.Install_salt()
            self.Init_sys()

    def main(self,options,args):
        try:
            if self.Sys() == "CentOS":
                if options.Set_hostname:
                    self.Set_hostname()
                if options.Change_ssh:
                    self.Change_ssh()
                if options.Check_openssl:
                    self.Check_openssl()
                if options.Add_user:
                    self.Add_user()
                if options.Install_salt:
                    self.Install_salt()
                if options.Init_sys:
                    self.Init_sys()
                if options.Mount_disk:
                    self.Mount_disk()
                if options.Init_all:
                    self.Init_all()
            else:
                print("only fit version as centos7.x")
                sys.exit()
        except Exception,e:
            print e

if __name__ == '__main__':
    usage = "usage: %prog [options] arg1 arg2 .. argn"
    parser = OptionParser(usage=usage)
    parser.add_option('-s','--Initialize-Set_hostname',action='store_true',dest='Set_hostname',default=False,help='Set up the hostname')
    parser.add_option('-j','--Initialize-Change_ssh',action='store_true',dest='Change_ssh',default=False,help='Change ssh port is 58422')
    parser.add_option('-k','--Initialize-Check_openssl',action='store_true',dest='Check_openssl',default=False,help='Checl openssl version and upgrade')
    parser.add_option('-l','--Initialize-Add_user',action='store_true',dest='Add_user',default=False,help='Add os-user for admin')
    parser.add_option('-m','--Initialize-Install_salt',action='store_true',dest='Install_salt',default=False,help='Install salt-minion and join as salt-master')
    parser.add_option('-n','--Initialize-Init_sys',action='store_true',dest='Init_sys',default=False,help='Upgrade yum epol')
    parser.add_option('-o','--Initialize-Initialize_disk',action='store_true',dest='Mount_disk',default=False,help='Initialize and mount disk')
    parser.add_option('-A','--Initialize-Init_all',action='store_true',dest='Init_all',default=False,help='Perform s-o all function')
    options,args = parser.parse_args()
    obj = init_os()
    obj.main(options,args)
