  #!/usr/bin/env python
# --*-- coding:utf-8 --*--
'''
手游渠道包，自动化批量分包脚本
'''

import proc
import subprocess
import os
import commands
from os import system
import time
from commands import getoutput
from random import choice
import hashlib
import sys
import time
import logging
from optparse import OptionParser
import urllib
import urllib2
import json

def writeLog(message):
    logger=logging.getLogger()
    filename = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    handler=logging.FileHandler("/tmp/"+"wuming-pkg-"+filename)
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)
    logger.info(message)

filepath = "/data/wuming/wuming.txt"
PATH = "/opt/rh/sdk/refresh.py"
SecretId = "AKIDqyLeRxfrzV7G2esxmH6VLmiEEnsMkDaB"
SecretKey = "Q1BjxeEaBsVmWtdsl4BREUJkdDBhlBbi"

def els(va):
    s = commands.getoutput("cat %s | awk 'NR==%s'" % (filepath,va))
    return s

def alarm(ret):
    post_url = 'http://ass.51.com/sms/sms4.php'
    postData  = {'problem':'pkg %s packaging of number is %s' % (els('1'),els('2')),'status':'%s' % ret,'host':'wuming'}
    req = urllib2.Request(post_url)
    response = urllib2.urlopen(req,urllib.urlencode(postData))
    print response.read()

filename = els('1')
chid = els('4')
begin = els('5')
end = els('6')

def clean():
    os.chdir("/data/apk/src/")
    if os.path.exists("%s.apk" % filename):
        system("rm -rf %s.apk" % filename)
        system("mv /data/wuming/*.apk /data/apk/src/%s.apk" % filename)
    else:
        print "file no such"
        system("mv /data/wuming/*.apk /data/apk/src/%s.apk" % filename)

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

def resign():
   clean()
   alarm("signature Start")
   os.chdir("/data/apk/src/")
   if os.path.exists(filename):
       run(['rm -rf %s' % filename])
   else:
       print "Continue to"
   run(['/data/apk/sign/apktool d %s.apk' % filename,'/data/apk/sign/apktool b %s' % filename])
   print "解压包完成"
   os.chdir("/data/apk/src/%s/dist/" % filename)
   run(['jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore /data/apk/sign/keystore/keystore -keypass 51.com -storepass 51.com -signedjar %s_signed.apk %s.apk 51.com' % (filename,filename),'mv %s_signed.apk /data/apk/tmp/%s.apk' % (filename,filename)])
   os.chdir("/data/apk/src/")
   run(['rm -rf %s' % filename])
   print "签名完成"

def md():
    os.chdir("/data/apk/work/")
    ret = getoutput("ls *")
    met = ret.split('\n')
    md_list = []
    for i in met:
       m = hashlib.md5()
       m.update(i)
       md_list.append(('%s' % m.hexdigest()))
    return md_list

def pkg():
   alarm("Packaging Start")
   os.chdir("/data/apk/pkg/")
   strs = ''
   for s in range(int(begin),int(end)):
      n = str(s)
      k = n.zfill(3)
      key = chid+str(k)+","+strs
      run(['java -jar batchpackapk.jar ../tmp/%s.apk ./ -c %s' % (filename,key)])
   run(['mv batchpack1*/* work/'])
   ret = getoutput("ls work/")
   cos = ret.split('\n')
   for item in cos:
      kvs = item.split('-')
      new_name = kvs[1].replace(".apk","") + '_' + kvs[0] + ".apk"
      run(['mv work/%s ../work/%s' % (item,new_name)])
   run(['rm -rf /data/apk/tmp/*','rm -rf batchpack1*'])
   md1 = md()[0]
   md2 = md()[-1]
   if md1 == md2:
      sys.exit(0)
      alarm("md5 check error!")
   alarm("Packaging End!")
   print "打包完成"

def upload_cos():
   alarm("upload Start")
   os.chdir("/data/apk/work/")
   dir = "/data/download%s" % els('3')
   if os.path.exists(dir):
      run(['mv * %s' % dir,'chown -R nobody:nobody %s' % dir])
   else:
      run(["mkdir -p %s" % dir])
      run(['mv * %s' % dir,'chown -R nobody:nobody %s' % dir])
   ret = getoutput("cat /data/cos/conf/config.ini | grep cos_path | awk '{print $3}'")
   run(["sed -i 's@%s@%s@g' /data/cos/conf/config.ini" % (ret,els('3'))])
   try:
      system("/bin/sh /data/cos/start_cos_sync.sh")
      print "上传完成"
      alarm("upload End")
   except Exception,e:
      print e

def refresh_cdn():
   s = range(int(begin),int(end))
   try:
      for i in s:
         n = str(i)
         k = n.zfill(3)
         url = "http://sdl.wuming.com%s/%s_%s%s.apk" % (els('3'),els('1'),chid,k)
         run(["python %s RefreshCdnUrl -u %s -p %s --urls %s" % (PATH,SecretId,SecretKey,url)])
      print "Refresh End"
      alarm("Refresh End")
      os.sleep(300)
   except Exception,e:
      print e

def preheating_cdn():
   s = range(int(begin),int(end))
   try:
      for i in s:
         n = str(i)
         k = n.zfill(3)
         url = "http://sdl.wuming.com%s/%s_%s%s.apk" % (els('3'),els('1'),chid,k)
         run(["php /opt/rh/sdk/preheating.php %s" % url])
      print "preheating End"
      alarm("preheating End")
      system("rm -rf /data/wuming/*")
   except Exception,e:
      print e


def main(options,args):
    try:
        if os.path.exists("/data/wuming/wuming.txt"):
            if options.resign:
                resign()
            if options.pkg:
                pkg()
            if options.upload_cos:
                upload_cos()
            if options.refresh_cdn:
                refresh_cdn()
            if options.preheating_cdn:
                preheating_cdn()
        else:
            print "no such file of wuming.txt"
    except Exception,e:
        writeLog(e)
        print e

if __name__ == '__main__':
    usage = "usage: %prog [options] arg1 arg2 .. argn"
    parser = OptionParser(usage=usage)
    parser.add_option('-r','--pkg-resign',action='store_true',dest='resign',default=False,help='autograph')
    parser.add_option('-p','--pkg-pkg',action='store_true',dest='pkg',default=False,help='The subcontract')
    parser.add_option('-u','--pkg-upload_cos',action='store_true',dest='upload_cos',default=False,help='upload')
    parser.add_option('-c','--pkg-refresh_cdn',action='store_true',dest='refresh_cdn',default=False,help='Refresh')
    parser.add_option('-s','--pkg-refresh_cdn',action='store_true',dest='preheating_cdn',default=False,help='preheating')
    options,args = parser.parse_args()
    main(options,args)
