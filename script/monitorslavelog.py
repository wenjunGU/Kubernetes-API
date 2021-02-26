#! /usr/bin/python
# -*- coding:utf-8 -*-

'''
数据库本地慢查日志监控;游戏服务器数据慢查日志监控
1分钟内慢查日志时间大于等于10s发短信报警通知
1分钟内慢查日志时间大于等于3s发邮件通知
'''
import os,datetime,sys,time
import re, datetime
from commands import *
import ConfigParser
import fcntl
import subprocess
import struct
import logging
import socket



host = "10.8.6.83"
key = "Query_time"
keys = "subtime"
keyse = "query_time1"
keyser = "lock_time1"



def getip(ethname):
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', ethname[:15]))[20:24])



logDir = '/var/log/runlog'


def datarecv_print(datarecv):
    for key in datarecv.keys():
        print "%s: %s" % (key, datarecv[key])



def get_output(cmd, removelf=''):
    ret = subprocess.Popen(cmd, shell=True, close_fds=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutdata, stderrdata = ret.communicate()
    if removelf != '':
        stdoutdata = stdoutdata.split('\n')[0]
    return stdoutdata, stderrdata


def getConfig(key, field='zabbixConfig'):
    global config_file_path
    iniName = 'monitorcoreConfig.ini'
    if config_file_path:
        if not os.path.exists(config_file_path):
            os.mkdir(config_file_path)
        iniPath = os.path.join(config_file_path, iniName)
    else:
        iniPath = os.path.join(sys.path[0], iniName)
    messages = read_config(iniPath, field, key)
    if messages:
        return messages
    return ''


def read_config(config_file_path, field, key):
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(config_file_path)
        result = cf.get(field, key).strip('"').strip("'")
        return result
    except Exception, e:
        print e
    return ''


def checkmysqlslavelog(log, mark_file):
    try:
        if os.path.exists(log):
            f_log = open(log, 'rw')
            if os.path.exists(mark_file):
                f_mark = open(mark_file,'r')
                mark = f_mark.read().split('|')[1]
                print "开始增量分析"
                f_log.seek(long(mark))
                f_content = f_log.read()
                mark = f_log.tell()
                f_mark.close()
                f_log.close()
                f_mark = open(mark_file,'w')
                f_mark.write(log + '|' + str(mark))
                f_mark.close()
            else:
                f_log.read()
                mark = f_log.tell()
                f_mark_file = open(mark_file, 'w')
                f_mark_file.write(log + '|' + str(mark))
                f_mark_file.close()
                f_log.close()
                print "初始化文件", log
                return
            Query_time_list = re.findall(r'.*Query_time:\s(\d{1,}\.\d{6}).*', f_content)
            Lock_time_list = re.findall(r'.*Lock_time:\s(\d{1,}\.\d{6}).*', f_content)
            if Query_time_list:
                ret_query_time = '%.2f' % float(max(Query_time_list))
                print "query_time",ret_query_time
                os.system("zabbix_sender -z %s -p 10051 -s \"%s\" -k \"%s\" -o %s" % ( host, getip('em2'), keyse, float(ret_query_time)))
            else:
                os.system("zabbix_sender -z %s -p 10051 -s \"%s\" -k \"%s\" -o %s" % ( host, getip('em2'), keyse, float(0)))
                print '没有匹配上'
            if Lock_time_list:
                ret_lock_time = '%.2f' % float(max(Lock_time_list))
                print "lock_time",ret_lock_time
                os.system("zabbix_sender -z %s -p 10051 -s \"%s\" -k \"%s\" -o %s" % ( host, getip('em2'), keyser, ret_lock_time))
            else:
                os.system("zabbix_sender -z %s -p 10051 -s \"%s\" -k \"%s\" -o %s" % ( host, getip('em2'), keyser, float(0)))
                print '没有匹配上'
        else:
            print "文件不存在：", log
            return
    except Exception, e:
        print "程序异常：", str(e)


def checkgameslavelog(path,logger):
    files = getupdatefile(path = path,time=5)
    if files:
        for file in files:
            mark_file = file + '.' + 'mark'
            text = getgamenewslavelog(file, mark_file)
            if text:
                Query_time_list = re.findall(r'.*time:(\d{1,})ms*', text)
                if Query_time_list:

                    ret_query_time = float(max(Query_time_list)) / 1000.0
                    ret = '%.2f'%ret_query_time
                    os.system("zabbix_sender -z %s -p 10051 -s \"%s\" -k \"%s\" -o %s" % ( host, getip('em2'), key, ret ))
                    logger.info('Warning File:%s Query_time:%s '%(file,ret))
                else:
                    print '没有匹配上'
    else:
        os.system("zabbix_sender -z %s -p 10051 -s \"%s\" -k \"%s\" -o %s" % ( host, getip('em2'), key, ret ))
        print "当前没有最新日志文件需要分析"

def getupdatefile(path,filetype='dbslowlog', time=2):
    now_time = datetime.datetime.now()
    # yes_time = now_time +datetime.timedelta(days=-1)
    now_time_nyr = now_time.strftime('%Y%m%d')
    file = '*' + filetype + '_' + now_time_nyr + '*' + '.log'
    files = getoutput("find %s -name '%s' -mmin -%d -print" % (path,file, time))
    if files:
        f_list = files.split('\n')
        print "当前分析日志文件:", str(f_list)
        return f_list
    else:
        return None


def getgamenewslavelog(log, mark_file):
    try:
        if os.path.exists(log):
            f_log = open(log, 'r')
            if os.path.exists(mark_file):
                f_mark = open(mark_file,'r')
                mark = f_mark.read().split('|')[1]
                print "开始增量分析..........."
                f_log.seek(long(mark))
                f_content = f_log.read()
                if not f_content:
                    return None
                mark = f_log.tell()
                f_log.close()
                f_mark.close()
                f_mark = open(mark_file,'w')
                f_mark.write(log + '|' + str(mark))
                f_mark.close()
                return f_content
            else:
                f_log.read()
                mark = f_log.tell()
                f_mark_file = open(mark_file, 'w')
                f_mark_file.write(log + '|' + str(mark))
                f_mark_file.close()
                f_log.close()
                print "初始化文件", log
                return None
        else:
            print "文件不存在：", log
            return None
    except Exception, e:
        print "程序异常：", str(e)

def removemodpid(piddir='/opt/run/',mod=''):
    filename='%s_run.pid' % mod
    file=os.path.join(piddir,filename)
    if os.path.isfile(file):
        os.remove(file)

def checkpidfile(piddir='/opt/run/',mod=''):
    filename='%s_run.pid' % mod
    file=os.path.join(piddir,filename)
    if os.path.isfile(file):
        return True
    else:
        return False
def savemodpid(piddir='/opt/run/',mod=''):
    mpid=str(os.getpid())
    filename='%s_run.pid' % mod
    file=os.path.join(piddir,filename)
    if not os.path.exists(piddir):
        os.makedirs(piddir)
    f=open(file,'w')
    f.write(mpid)
    f.close
    return True

if __name__ == '__main__':

    mysqlslavelog = '/var/log/mysql/slowlog/slowquery.log'
    mark_file = mysqlslavelog + '.'+'mark'
    modname = 'monitorslavelog.py'
    gameslavepath ='/game/log/op/db'
    tim = "180"
   

    cmd = 'ntpdate -d 10.1.1.22'
    cmp = "date'+%Y%m%d %H:%M:%S'"
    ret,ITxiaopang = get_output(cmd)
    if ret:
      subtime = ret.strip().split('\n')[-1].split('offset')[-1].split('sec')[0].strip().replace('-','')
      print '与ntp服务器时间误差：%s' % ( subtime )
    if subtime >= tim or subtime <= tim:
      os.system("zabbix_sender -z %s -p 10051 -s \"%s\" -k \"%s\" -o %s" % ( host, getip('em2'), key, subtime ))
    else:
      print "异常信息: %s " % (ITxiaopang)

    try:
        if not os.path.exists(logDir):
            os.mkdir(logDir,0777)
        logger = logging.getLogger()
        logPath = os.path.join(logDir,'monitorslavelog.log')
        hdl = logging.FileHandler(logPath)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdl.setFormatter(formatter)
        logger.addHandler(hdl)
        logger.setLevel(logging.INFO)
    except Exception,e:
        print  e

    if len(sys.argv) < 2:
        print 'No action specified.'
        sys.exit()
    if sys.argv[1].startswith('--'):

        if not checkpidfile(mod=modname):
            savemodpid(mod=modname)
        else:
            print '进程已经存在: %s' %modname
            sys.exit()
        try:
            option = sys.argv[1][2:]
            if option == 'mysql':
                checkmysqlslavelog(mysqlslavelog,mark_file)
                removemodpid(mod=modname)
            elif option == 'game':
                checkgameslavelog(gameslavepath,logger)
                removemodpid(mod=modname)
            else:
                print 'Unknown option.'
                sys.exit()
        except:
            if checkpidfile(mod=modname):
                removemodpid(mod=modname)
