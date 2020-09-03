#!/usr/bin/env python  
# coding: utf-8  
  
import ping  
import sys  
  
try:  
  result = ping.quiet_ping('www.google.com', timeout=2, count=10, psize=64)  
  if int(result[0]) == 100:  
    print 'Critical - 宕机, To www.google.com 丢包率:%s%%' % (result[0])  
    #sys.exit(2)  
  else:  
    max_time = round(result[1], 2)  
    if int(result[0]) < int(50) and int(result[1]) < int(100):  
      print 'OK - To www.google.com 丢包率:%s%%, 最大响应时间:%s ms' % (result[0],max_time)  
      #sys.exit(0)  
    elif int(result[0]) >= int(50) or int(result[1]) >= int(100):  
      print 'Warning - To www.google.com 丢包率:%s%%, 最大响应时间:%s ms' % (result[0], max_time)  
      #sys.exit(1)  
    else:  
      print 'Unknown'  
      #sys.exit(3)  
except IndexError,e:
    print(e)  
