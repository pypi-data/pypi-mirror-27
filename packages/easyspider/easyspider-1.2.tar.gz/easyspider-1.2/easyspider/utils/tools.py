#coding=utf-8
import time

def parse_time(timestamp):
	try:
		return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timestamp))
	except Exception,e:
		return "0000-00-00 00:00:00"


def get_time():
    return parse_time(time.time())

if __name__ == '__main__':
	print get_time()