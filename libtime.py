#!/usr/bin/python
#!-*-coding:utf-8-*-
import time
import datetime

#transfer time to 2012_02_12
def trans_cur():
	t=datetime.date.today()
	return str(t).replace('-','_')
#2012-09-02
def get_str_date():
	t = datetime.date.today()
	return str(t)
#parse 19970101/1997-01-01
def parseTime(t_str):
		t = ""
		if t_str != "":
			if '-' in t_str:
				t = time.strptime(t_str, "%Y-%m-%d")
			else:
				t = time.strptime(t_str,"%Y%m%d")
		else:
			t = time.strptime("1997-01-01", "%Y-%m-%d")
		d = datetime.datetime(* t[:6])
		return d
def get_localtime_str():
	tstp = time.time()
	timestruct = time.localtime(tstp)
	#2016-12-22 10:49:57
	lt_str = time.strftime('%Y-%m-%d %H:%M:%S',timestruct)
	return lt_str