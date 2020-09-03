#!/usr/bin/env Python
# --*-- coding:utf-8 --*--

from __future__ import print_function
from collections import OrderedDict
 
def meminfo():
    ''' Return the information in /proc/meminfo
    as a dictionary '''
    meminfo=OrderedDict()
 
    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo
 
if __name__=='__main__':
    #print(meminfo())
    meminfo = meminfo()
    print('Total memory: {0}'.format(meminfo['MemTotal']))
    print('Free memory: {0}'.format(meminfo['MemFree']))

[root@WJ-SZ-WEB-TEST ~]# cat mima.py 
#!/usr/bin/env python
# --*-- coding:utf-8 --*--

from sys import argv
import random,string,os,datetime
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkpolardb.request.v20170801.CreateAccountRequest import CreateAccountRequest

class init_sql(object):

    def __init__(self):
        self.accessKeyId = "LTAI4FihLAXFoxptrAs6EQBT"
        self.accessSecret = "ki7QF49BHgaXQQEuwtZy729qYreMJL"
        self.region = "cn-shanghai"
        self.rs = "dbreadonly"
        self.ws = "dbreadwrite"
        self.plat = "platconf"
        self.RdsId = argv[1]

    def __Get_time(self):
        now = datetime.datetime.now()
        info = now.strftime('%Y-%m-%d_%H:%M:%S')
        return(info)

    def __Write_fs(self,name,passwd):
        file_path = "{0}/{1}.txt".format(os.getcwd(),self.__Get_time())
        with open(file_path, 'a+') as f:
            f.write(str("{0}: {1}".format(name,passwd)) + '\n')

    def __Secret(self):
        src = string.ascii_letters + string.digits
        list_passwds = []
        list_passwd_all = random.sample(src, 16)
        list_passwd_all.extend(random.sample(string.digits, 1))
        list_passwd_all.extend(random.sample(string.ascii_lowercase, 1))
        list_passwd_all.extend(random.sample(string.ascii_uppercase, 1))
        random.shuffle(list_passwd_all)
        str_passwd = ''.join(list_passwd_all)
        if str_passwd not in list_passwds:
            list_passwds.append(str_passwd)
        for i in list_passwds:
            return i

    def __Create_polo(self,dbid,dbname,dbpass,type):
        client = AcsClient(self.accessKeyId, self.accessSecret, self.region)
        request = CreateAccountRequest()
        request.set_accept_format('json')
        request.set_DBClusterId(str(dbid))
        request.set_AccountName(str(dbname))
        request.set_AccountPassword(str(dbpass))
        request.set_AccountType(str(type))
        response = client.do_action_with_exception(request)
        return(response)

    def CreateAccount_polardb_super(self):
        try:
            dbpass = raw_input("please input dbname password:")
            if dbpass != "" and self.RdsId != "":
                self.__Create_polo(self.RdsId,"dbadmin",dbpass,"Super")
                print("Super account apply secc!")
            else:
                print("please check input")
        except Exception,e:
            print(e)

    def CreateAccount_polardb_normal(self):
        names = [self.rs,self.ws,self.plat]
        for i in names:
            if self.RdsId != "":
                self.__Create_polo(self.RdsId,i,self.__Secret(),"Normal")
                self.__Write_fs(i,self.__Secret())
            else:
                print("please check input")



obj = init_sql()
obj.CreateAccount_polardb_super()
