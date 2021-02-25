#!/usr/bin/env  python
# --*-- coding:UTF-8 --*--
import  sys
import  tab
import  re
import  os
import  time
from docker  import Client
import  commands
keys_container_stats_list = ['blkio_stats', 'precpu_stats', 'network', 'read', 'memory_stats', 'cpu_stats']
merit_list=['usage','limit','mem_use_percent','total_cpu_usage','system_cpu_usage','cpu_usage_percent','rx_bytes','tx_bytes']
returnval = None
def start(container_name):
    global container_stats
    conn=Client(base_url='unix://run/docker.sock',version='1.19')
    generator=conn.stats(container_name)
    try:
        container_stats=eval(generator.next())
    except NameError,error_msg:
        pass
#        print error_msg
        container_stats=eval(generator.next())
    finally:
        conn.close()
def monitor_docker(monitor_item,merit):
    if merit == 'mem_use_percent':
        start(container_name)
        mem_usage = container_stats['memory_stats']['usage']
        mem_limit = container_stats['memory_stats']['limit']
        returnval = round(float(mem_usage) / float(mem_limit),2)
        print  returnval
    elif merit == 'system_cpu_usage':
        start(container_name)
        first_result = container_stats['cpu_stats']['system_cpu_usage']
        start(container_name)
        second_result = container_stats['cpu_stats']['system_cpu_usage']
        returnval = second_result - first_result
        print  returnval
    elif merit == 'total_cpu_usage':
        start(container_name)
        first_result = container_stats['cpu_stats']['cpu_usage']['total_usage']
        start(container_name)
        second_result = container_stats['cpu_stats']['cpu_usage']['total_usage']
        returnval = second_result - first_result
        print returnval
    elif merit == 'cpu_usage_percent':
        start(container_name)
        system_use=container_stats['cpu_stats']['system_cpu_usage']
        total_use=container_stats['cpu_stats']['cpu_usage']['total_usage']
        cpu_count=len(container_stats['cpu_stats']['cpu_usage']['percpu_usage'])
        returnval = round((float(total_use)/float(system_use))*cpu_count*100.0,2)
        print returnval
    elif merit == 'rx_bytes':
        command='''docker  exec -it  api1  ifconfig eth1 | grep "bytes"  | awk '{print $2}' | awk -F ':' '{print $2}' '''
        result_one = commands.getoutput(command)
        time.sleep(1)
        command='''docker  exec -it  api1  ifconfig eth1 | grep "bytes"  | awk '{print $2}' | awk -F ':' '{print $2}' '''
        result_second = commands.getoutput(command)
        returnval = round((int(result_second)  -  int(result_one))/1024,2)
        print returnval
    elif merit == 'tx_bytes':
        command='''docker  exec -it  api1  ifconfig eth1 | grep "bytes"  | awk '{print $6}' | awk -F ':' '{print $2}' '''
        result_one = commands.getoutput(command)
        time.sleep(1)
        command='''docker  exec -it  api1  ifconfig eth1 | grep "bytes"  | awk '{print $6}' | awk -F ':' '{print $2}' '''
        result_second = commands.getoutput(command)
        returnval = round((int(result_second)  -  int(result_one))/1024,2)
        print returnval
if __name__ == '__main__':
    command='''docker ps | awk '{print $NF}'| grep -v "NAMES"'''
    str=commands.getoutput(command)
    container_counts_list=str.split('\n')
    if sys.argv[1] not in container_counts_list:
        print container_counts_list
        print "你输入的容器名称错误，请重新执行脚本，并输入上述正确的容器名称."
        sys.exit(1)
    else:
        container_name = sys.argv[1]
        if sys.argv[2] not in keys_container_stats_list:
            print keys_container_stats_list
            print '你输入的容器监控项不在监控范围，请重新执行脚本，并输入上述正确的监控项.'
            sys.exit(1)
        else:
            monitor_item = sys.argv[2]
            if sys.argv[3] not in merit_list:
                print merit_list
                print "你输入的容器监控明细详细不在监控范围内，请重新执行脚本，并输入上述正确的明细监控指标."
            else:
                merit = sys.argv[3]
                monitor_docker(monitor_item,merit)
