#!/usr/bin/python
#!-*-coding:utf-8-*-
from liblog import selflog
import gzip
import os
import zipfile
#logobj=selflog('../logs/libfile.log')
#myLogger=logobj.getLogger()
def rmfiles(dictionary):
	try:
		#cur_dir=os.getcwd()
		data_dir=dictionary#"{}/{}".format(cur_dir,dictionary)
		print 'Delete files in [{}]'.format(data_dir)
		files = os.listdir(data_dir)
		print "files:{}".format(str(files))
		for fp in files:
			fdir="{}/{}".format(data_dir,fp)
			if os.path.exists(fdir):
				os.system('rm '+fdir)
			print "{} deleted...".format(fdir)
		info = "{} files are deleted...".format(str(files))
		return (0,info)
	except Exception,e:
		info = "libfile.py:{}".format(str(e))
		#myLogger.debug(str(e))
		print str(e)
		return (1,info)
def ungzfile(fdir,des_name):
	try:
		with gzip.open(fdir, 'rb') as infile:
			with open(des_name, 'wb') as outfile:
				for line in infile:
					outfile.write(line)
		return (des_name,"Unzip successful:{}".format(des_name))
	except Exception,e:
		print str(e)
		return (None,str(e))
def unzipfile(fdir,desdir):
	#r = zipfile.is_zipfile(fdir)
	#if r:
	try:
		fz=zipfile.ZipFile(fdir,'r')
		for f in fz.namelist():
			fz.extract(f,desdir)
		return (fz.namelist(),"Unzip successful:{}".format(desdir))
	#else:
	except Exception,e:
		return (None,str(e))
