#!/usr/bin/env python
# --*-- coding:utf-8 --*--

import fcntl,struct
from os import system
import os,re,time,datetime
import socket,time
from commands import getoutput
import subprocess,paramiko

APATH = '/home/zyadmin/mnkj'
PATH = '/home/zyadmin/mnkj/alms.txt'
pids = {
        'tcp':'8647',
        'mbrtu':'8651',
        'mbtcp':'8655',
        'mqtt':'8660'
};

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        yield self.match
        raise StopIteration

    def match(self, *args):
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False

class main(object):

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

    def logs(self,data):
        file = open('/home/zyadmin/mnkj/log/ziyu.log','a')
        file.write(data)
        file.close()

    def get_time(self):
        now = datetime.datetime.now()
        info = now.strftime('%Y-%m-%d %H:%M:%S')
        return info

    def exec_sftp(self): 
        try:                                                                                                                                                 
            private_key = paramiko.RSAKey.from_private_key_file('/home/zyadmin/.ssh/id_rsa')                                                                                 
            trans = paramiko.Transport(('10.173.193.16', 40022))                                                                                                        
            trans.connect(username='zyadmin', pkey=private_key)                                                                                                         
            sftp = paramiko.SFTPClient.from_transport(trans)                                                                                                         
            sftp.get(remotepath='/home/wind/java/alarm_log/alarm.log', localpath='/home/zyadmin/mnkj/alarm.log')
            trans.close()
        except Exception,e:                                                                                                                                  
            print e

    def file_fenxi(self):
        num = getoutput("wc -l %s/alarm.log | awk '{print $1}'"%APATH)
        nums = getoutput("cat %s/alm.txt"%APATH)
        if str(num) == str(nums):
            obj.logs('{0}:暂无最新告警\n'.format(obj.get_time()))
            print("暂无最新报警")
            exit(0)
        else:
            info = int(num) - int(nums)
            obj.exec_run(["tail -%s %s/alarm.log > %s/alms.txt"%(info,APATH,APATH),"echo %s > %s/alm.txt"%(num,APATH)])

    def check_port(self,ip='127.0.0.1',port='22'):
            sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sk.settimeout(1)
            try:
                sk.connect((str(ip),int(port)))
                return 'OK'
            except Exception:
                return 'Fail'
            sk.close()

    def check_log(self):
        now = datetime.datetime.now()
        new_time = now - datetime.timedelta(minutes = 10)
        info = getoutput("sed -n '/%s/,/%s/p' /var/log/cmd_track.log > %s/log.txt"%(new_time.strftime('%Y-%m-%d %H:%M'),now.strftime('%Y-%m-%d %H:%M'),APATH))
        number = getoutput("cat  {0}/log.txt | egrep 'pkill|kill' | grep -Ev 'grep'".format(APATH))
        if number == '':
            return 'OK'
        else:
            return 'Fail'

    def perform(self,shell):
        pid = getoutput("ps -ef | grep %s | grep -Ev 'grep' | awk '{print $2}'" % shell)
        system("kill %s" % pid)
        time.sleep(20)                                                                                                                                 
        os.chdir('/home/wind/java/')                                                                                                                   
        system("nohup java -jar %s&" % shell)                                                                                                      
        if obj.check_port(port=pids[obj.get_filter()]) == 'OK':                                                                                                
            print("process is running")                                                                                                                
            system("rm -rf %s" % PATH)                                                                                                                 
            exit(0)
        else:                                                                                                                                          
            obj.logs("{0}:服务{1}自愈失败\n".format(obj.get_time(),shell))

    def run(self):
        if obj.check_log() == 'OK' and obj.check_port(port=pids[obj.get_filter()]) == 'OK':
            for case in switch(obj.get_filter()):
               if case('tcp'):
                  obj.perform('tcp_server.jar')
                  obj.logs('{0}:服务tcp_server.jar自愈完成\n'.format(obj.get_time()))
               if case('mbrtu'):
                  obj.perform('modbus_rtu.jar')
                  obj.logs('{0}:服务modbus_rtu.jar自愈完成\n'.format(obj.get_time()))
               if case('mbtcp'):
                  obj.perform('modbus_tcp.jar')
                  obj.logs('{0}:服务modbus_tcp.jar自愈完成\n'.format(obj.get_time()))
               if case('mqtt'):
                  pid = getoutput("ps -ef | grep 'mqtt_server.jar' | grep -Ev 'grep' | awk '{print $2}'")
                  system("kill %s" % pid)
                  time.sleep(10)
                  system("/home/wind/emqttd/bin/emqttd stop")
                  time.sleep(10)
                  system("/home/wind/emqttd/bin/emqttd start")
                  time.sleep(10)
                  os.chdir('/home/wind/java/')
                  system("nohup java -jar mqtt_server.jar&")
                  if obj.check_port(port=pids[obj.get_filter()]) == 'OK':
                      print("process is running")
                      obj.logs('{0}:服务mqtt_server.jar自愈完成\n'.format(obj.get_time()))
                      system("rm -rf %s" % PATH)
                      exit(0)
                  else:
                      obj.logs("{0}:服务mqtt_server.jar自愈失败\n".format(obj.get_time()))
               if case():
                   print "something else"
                   obj.logs('{0}:进程:{1}不在自愈范围\n'.format(obj.get_time(),obj.get_filter()))
        else:
            print "系统判断人为操作,进程结束"
            obj.logs('{0}:系统判断人为操作，进程结束\n'.format(obj.get_time()))

    def get_filter(self):
        if os.path.exists(PATH):
            f = open(PATH)
            line = f.readline()
            while line:
                line = line.replace('10分钟无数据上行,请检查连接程序','')
                line = line.split()
                for i in line:
                    i = re.sub('[^a-zA-Z]','',i)
                    return i
                line = f.readline()
            f.close()                                                                                                                                            
        else:
            print "No such failter file"

    def getip(self,ethname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', ethname[:15]))[20:24])
        return ip[-2:]

    def get_host(self):
        obj.exec_sftp()
        if os.path.exists('%s/alm.txt'%APATH) and os.path.exists('%s/log.txt'%APATH):
            obj.file_fenxi()
            if os.path.exists(PATH):
                f = open(PATH)
                line = f.readline()
                while line:
                    line = line.replace('10分钟无数据上行,请检查连接程序','')
                    line = line.split()
                    for i in line:
                        i = re.findall(r"\d+\.?\d*",i)
                        for m in i:
                            if m == obj.getip('eth1'):
                                obj.run()
                            else:
                                print("不是本机,跳过执行体")
                                obj.logs('{0}:不是本机，跳过执行体\n'.format(obj.get_time()))
                    line = f.readline()
                f.close()
            else:
                print "无告警触发条件!"
                obj.logs('{0}:无告警触发条件\n'.format(obj.get_time())) 
        else:
            num = getoutput("wc -l %s/alarm.log | awk '{print $1}'"%APATH)                                                                                   
            values = getoutput("wc -l /var/log/cmd_track.log | awk '{print $1}'")                                                                            
            obj.exec_run(["echo %s > %s/alm.txt"%(num,APATH),"echo %s > %s/log.txt"%(values,APATH)])                                                         
            print("初始化系统分析环境")

if __name__ == '__main__':
    obj = main()
    obj.get_host()
