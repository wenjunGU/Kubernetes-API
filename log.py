#!/usr/bin/env python
# --*-- coding:utf-8--*--

import subprocess
from commands import getoutput
import paramiko

def run(cmd):
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

def fenxi():
    num = getoutput("wc -l /root/alarm.log | awk '{print $1}'")
    nums = getoutput("cat /root/alm.txt")
    if num == nums:
        print("暂无最新报警")
        return 0
    else:
        run(["tail -{0} /root/alarm.log > /root/alms.txt".format(fenxi()),"echo {0} > /root/alm.txt".format(info)]])

#fenxi()
#chuli()

#info = getoutput("tail -3 /root/alms.txt")
#info = info.replace('分钟无数据上行,请检查连接程序','')
#print info

def exec_command():
        private_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname='172.16.252.48', port=int(22), username='root', pkey=private_key, timeout=1)
            stdin, stdout, stderr = ssh.exec_command('touch /tmp/paramiko.txt')
            print(stdout.read().decode())
        except Exception,e:
            print e
        ssh.close()

def sftp():
    private_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')
    trans = paramiko.Transport(('172.16.252.48', 22))
    trans.connect(username='root', pkey=private_key)
    sftp = paramiko.SFTPClient.from_transport(trans)
    sftp.get(remotepath='/tmp/check_disk.py', localpath='/tmp/check_disk.py')
    trans.close()

sftp()
