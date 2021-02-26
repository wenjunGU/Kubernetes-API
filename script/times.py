import time
import datetime

dt = "2019-03-25T17:27:07.170507764+08:00"
time_array = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
timestamp = time.mktime(time_array.timetuple())
stime = float(JDtime) + timestamp
dt_new = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(float(stime)))
print dt_new
