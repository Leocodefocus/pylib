#!-*-coding:utf-8-*-
#!/usr/bin/env python

import urllib
import os
from liblog import selflog
#logobj=selflog('../logs/rsmdown.log')
#myLogger=logobj.getLogger()
TARGET_URL = 'http://mirror1.malwaredomains.com/files/'
TARGET_FILE = 'domains.txt'
FILE_PATH='.'
class CustomURLOpener(urllib.FancyURLopener):
	"""Override FancyURLopener to skip error 206 (when a
		partial file is being sent)
	"""
	def http_error_206(self,url,fp,errrcode,errmsg,headers,data=None):
		pass

def resume_download(TARGET_URL,TARGET_FILE,FILE_PATH):
	file_exists = 0
	loop=1
	CustomURLClass = CustomURLOpener()
	fp="{}/{}".format(FILE_PATH,TARGET_FILE)
	try:
		if os.path.exists(fp):
			out_file = open(fp,"ab")
			file_exists = os.path.getsize(fp)
			#if the file exists,then only download the unfinished part
			CustomURLClass.addheader("range","bytes=%s-"%(file_exists))

		else:
			print "file 不存在"
			out_file = open(fp,"wb")
		print "[{}][{}]".format(TARGET_URL,TARGET_FILE)
		web_page = CustomURLClass.open(TARGET_URL+TARGET_FILE)
	
		#Check if last download was OK
		print "tar length:%s..." % web_page.headers['Content-Length']
		print "file exists length:%s..." % file_exists
		if int(web_page.headers['Content-Length']) == int(file_exists):
			loop = 0
			print "File alrady downloaded!"

		byte_count = 0
		while loop:
			data = web_page.read(8192)
			if not data:
				break
			out_file.write(data)
			byte_count = byte_count + len(data)
			print "Complete %d....remain %d" % ((int(file_exists)+byte_count),(int(web_page.headers['Content-Length'])-(int(file_exists)+byte_count)))
		web_page.close()
		out_file.close()
		print "Completed....................."
		for k,v in web_page.headers.items():
			print k,"=",v
		print "File copied {} bytes from {}".format(str(byte_count),web_page.url)
		return (0,"File copied {} bytes from {}".format(str(byte_count),web_page.url))
	except Exception,e:
		return (1,str(e))
if __name__=='__main__':
	resume_download('https://static.nvd.nist.gov/feeds/xml/cve/2.0/','nvdcve-2.0-2016.xml.zip','.')
