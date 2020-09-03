#!/usr/bin/env python
# --*-- coding:utf-8 --*--

'''
time:2019-11-20
user:wenjun.gu
role:阿里云RDS/POLOARDB初始化工具，自动创建库表、超级用户以及权限用户
project:NXX
##执行步骤：python init_sql.py -r/p「-r初始化目标为rds，-p初始化目标为polardb」「RDS或者POLARDB的访问地址」「RDS或者POLOARDB的唯一标识ID」
##严重依赖阿里云SDK
'''

from sys import argv
import random,string,os,datetime,json,sys,time
from commands import getoutput as gt
from optparse import OptionParser
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkpolardb.request.v20170801.CreateAccountRequest import CreateAccountRequest
from aliyunsdkpolardb.request.v20170801.GrantAccountPrivilegeRequest import GrantAccountPrivilegeRequest
from aliyunsdkpolardb.request.v20170801.DescribeDatabasesRequest import DescribeDatabasesRequest
from aliyunsdkrds.request.v20140815.CreateAccountRequest import CreateAccountRequest as CreateAccount
from aliyunsdkrds.request.v20140815.DescribeDatabasesRequest import DescribeDatabasesRequest as DescribeDatabases
from aliyunsdkrds.request.v20140815.GrantAccountPrivilegeRequest import GrantAccountPrivilegeRequest as GrantAccountPrivilege

class init_polardb(object):                                     ##POLARDB初始化类

    def __init__(self):
        self.accessKeyId = "LTAI4FihLAXFoxptrAs6EQBT"           ##阿里云数据库管控AK
        self.accessSecret = "ki7QF49BHgaXQQEuwtZy729qYreMJL"    ##阿里云数据库管控秘钥
        self.region = "cn-shanghai"                             ##数据库开通地域，此三项按照实际需求修改
        self.rs = "dbreadonly"
        self.ws = "dbreadwrite"
        self.plat = "platconf"
        self.rs_pass = self.Secret__()
        self.ws_pass = self.Secret__()
        self.plat_pass = self.Secret__()
        self.Dbaddr = argv[2]
        self.RdsId = argv[3]
        self.Dbadmin_passwd = self.Secret__()

    def Get_time__(self):                               ##获取当前时间，精确到小时
        now = datetime.datetime.now()
        info = now.strftime('%Y-%m-%d_%H')
        return(info)

    def Write_fs__(self,name,passwd):                  ##数据写入函数
        file_path = "{0}/{1}.txt".format(os.getcwd(),self.Get_time__())
        with open(file_path, 'a+') as f:
            f.write(str("{0}: {1}".format(name,passwd)) + '\n')

    def Grant_Account_polo__(self,name,db_name,auth_type):                      ##调用阿里云权限授予SDK
            client = AcsClient(self.accessKeyId, self.accessSecret, self.region)
            request = GrantAccountPrivilegeRequest()
            request.set_accept_format('json')
            request.set_DBClusterId(self.RdsId)
            request.set_AccountName(name)
            request.set_DBName(db_name)
            request.set_AccountPrivilege(auth_type)
            response = client.do_action_with_exception(request)
            return(response)

    def Secret__(self):                                                         ##生成16位密码函数，密码复杂度可自定义
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

    def Get_polo_dbname__(self):                                            ##调用阿里云获取库表SDK
        client = AcsClient(self.accessKeyId, self.accessSecret, self.region)
        request = DescribeDatabasesRequest()
        request.set_accept_format('json')
        request.set_DBClusterId(self.RdsId)
        response = client.do_action_with_exception(request)
        new_dict = json.loads(response, encoding='utf-8')
        dbname_list = []
        for d in new_dict.get('Databases').get('Database'):
            dbname = d.get('DBName')
            dbname_list.append(dbname)
        dbname_str = map(str, dbname_list)
        return(dbname_str)

    def Create_polo__(self,dbid,dbname,dbpass,type):                        ##调用阿里云用户创建SDK
        client = AcsClient(self.accessKeyId, self.accessSecret, self.region)
        request = CreateAccountRequest()
        request.set_accept_format('json')
        request.set_DBClusterId(str(dbid))
        request.set_AccountName(str(dbname))
        request.set_AccountPassword(str(dbpass))
        request.set_AccountType(str(type))
        response = client.do_action_with_exception(request)
        return(response)

    def CreateAccount_polardb_super(self):                                  ##创建DBADMIN高权限账户
        try:
            if self.RdsId != "" and self.Dbaddr != "" and self.Dbadmin_passwd != "":
                self.Create_polo__(self.RdsId,"dbadmin",self.Dbadmin_passwd,"Super")
                self.Write_fs__("dbadmin",self.Dbadmin_passwd)
                print("Super AccountUser dbadmin apply secc!")
            else:
                print("please check input")
                sys.exit()
        except Exception,e:
            print(e)

    def CreateAccount_polardb_normal(self):                                 ##创建读写权限账户
        names = [self.rs,self.ws,self.plat]
        npass = [self.rs_pass,self.ws_pass,self.plat_pass]
        for i in range(0,len(names)):
            if self.RdsId != "" and self.Dbaddr != "":
                self.Create_polo__(self.RdsId,names[i],npass[i],"Normal")
                self.Write_fs__(names[i],npass[i])
                print("Normal AccountUser %s apply secc!" % names[i])
            else:
                print("please check input")

    def Grant_Account_polo(self):                                           ##为读写权限账户授权
        try:
            for i in self.Get_polo_dbname__():
                self.Grant_Account_polo__(self.rs,i,"ReadOnly")
                self.Grant_Account_polo__(self.ws,i,"ReadWrite")
            self.Grant_Account_polo__(self.plat,"db_nxx_conf","ReadWrite")
        except Exception,e:
            print(e)

    def INIT(self):                                                         ##执行主体
        self.CreateAccount_polardb_super()
        self.CreateAccount_polardb_normal()
        time.sleep(15)
        if run().Source_Sql(self.Dbaddr,self.Dbadmin_passwd) == "True":
            self.Grant_Account_polo()

class init_rsd(object):                                                     ##RDS初始化类

    def __init__(self,objs = init_polardb()):
        self.objss = objs
        self.Rds_dbpasswd = init_polardb().Secret__()

    def __Create_rds(self,dbid,dbname,dbpass,type):
        client = AcsClient(init_polardb().accessKeyId, init_polardb().accessSecret, init_polardb().region)
        request = CreateAccount()
        request.set_accept_format('json')
        request.set_DBInstanceId(str(dbid))
        request.set_AccountName(str(dbname))
        request.set_AccountPassword(str(dbpass))
        request.set_AccountType(str(type))
        response = client.do_action_with_exception(request)
        return(response)

    def __Get_rds_dbname(self):
        client = AcsClient(init_polardb().accessKeyId, init_polardb().accessSecret, init_polardb().region)
        request = DescribeDatabases()
        request.set_accept_format('json')
        request.set_DBInstanceId(init_polardb().RdsId)
        response = client.do_action_with_exception(request)
        new_dict = json.loads(response, encoding='utf-8')
        dbname_list = []
        for d in new_dict.get('Databases').get('Database'):
            dbname = d.get('DBName')
            dbname_list.append(dbname)
        dbname_str = map(str, dbname_list)
        return(dbname_str)

    def __Grant_Account_rds(self,name,db_name,auth_type):
            client = AcsClient(init_polardb().accessKeyId, init_polardb().accessSecret, init_polardb().region)
            request = GrantAccountPrivilege()
            request.set_accept_format('json')
            request.set_DBInstanceId(init_polardb().RdsId)
            request.set_AccountName(name)
            request.set_DBName(db_name)
            request.set_AccountPrivilege(auth_type)
            response = client.do_action_with_exception(request)
            return(response)

    def CreateAccount_rds_super(self):
        try:
            if init_polardb().RdsId != "" and init_polardb().Dbaddr != "" and self.Rds_dbpasswd != "":
                self.__Create_rds(init_polardb().RdsId,"dbadmin",self.Rds_dbpasswd,"Super")
                init_polardb().Write_fs__("dbadmin",self.Rds_dbpasswd)
                print("Super AccountUser dbadmin apply secc!")
            else:
                print("please check input")
                sys.exit()
        except Exception,e:
            print(e)

    def CreateAccount_rds_normal(self):
        names = [init_polardb().rs,init_polardb().ws,init_polardb().plat]
        npass = [init_polardb().rs_pass,init_polardb().ws_pass,init_polardb().plat_pass]
        for i in range(0,len(names)):
            if init_polardb().RdsId != "" and init_polardb().Dbaddr != "":
                self.__Create_rds(init_polardb().RdsId,names[i],npass[i],"Normal")
                init_polardb().Write_fs__(names[i],npass[i])
                print("Normal AccountUser %s apply secc!" % names[i])
            else:
                print("please check input")

    def Grant_Account_rds(self):
        try:
            for i in self.__Get_rds_dbname():
                self.__Grant_Account_rds(init_polardb().rs,i,"ReadOnly")
                self.__Grant_Account_rds(init_polardb().ws,i,"ReadWrite")
            self.__Grant_Account_rds(init_polardb().plat,"db_nxx_conf","ReadWrite")
            print("Grant Account apply secc!")
        except Exception,e:
            print(e)

    def INIT(self):
        self.CreateAccount_rds_super()
        self.CreateAccount_rds_normal()
        time.sleep(30)
        if run().Source_Sql(init_polardb().Dbaddr,self.Rds_dbpasswd) == "True":
            self.Grant_Account_rds()

class run(object):                                                  ##组装POLARDB和RDS两个类

    def Source_Sql(self,host,passwd):                               ##为POLARDB和RDS建库建表函数
        Sql_list = gt("ls sql/* | grep '.sql'")
        if not Sql_list is None:
            for i in Sql_list.split():
                os.system("mysql -udbadmin -h {0} -p{1} < {2}".format(host,passwd,i))
            print("MysqlDump is True")
            return ("True")
        else:
            print("MysqlDump is Fail")
            sys.exit()

    def main(self,options,args):                                    ##提供参数功能
        try:
            if options.init_polardb:
                init_polardb().INIT()
            if options.init_rds:
                init_rsd().INIT()
        except Exception,e:
            print(e)

if __name__ == '__main__':
    usage = "usage: %prog [options] arg1 arg2 .. argn"
    parser = OptionParser(usage=usage)
    parser.add_option('-r','--Initialize-rds',action='store_true',dest='init_rds',default=False,help='Initialize for rds')
    parser.add_option('-p','--Initialize-polardb',action='store_true',dest='init_polardb',default=False,help='Initialize for polardb')
    options,args = parser.parse_args()
    obj = run()
    obj.main(options,args)
