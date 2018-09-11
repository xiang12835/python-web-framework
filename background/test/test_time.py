# coding=utf-8


import datetime

t1 = "2018-08-09 00:00:00"

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def string_to_datetime(datetime_str, _format=DATE_TIME_FORMAT):
    return datetime.datetime.strptime(datetime_str, _format)


t1 = string_to_datetime(t1)

n = datetime.datetime.now()


print n
print t1

print 11*3600+50*60+33
d = n - t1

seconds = d.seconds  # 当天的秒数
total_seconds = d.total_seconds()  # 总秒数

print seconds
print total_seconds
print type(total_seconds)


