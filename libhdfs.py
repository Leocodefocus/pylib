#!/usr/bin/python
#!-*-coding:utf-8-*-
##############################################################
"""
  FileName : pyhdfs.py
  Author : Li Jishuai
  mUser:Zhao Chunhui
  Date : 2016-11-16
  His : 1.1
  Description :
     基于python hdfs库,提供常用的hdfs操作,包括:
     1) 查看指定的hdfs目录
     2) 从指定目录下载文件
     3) 上传文件到指定目录
     4) 重命名目录
	 5) 写数据到指定文件
     6) 判断目录或者文件是否存在
     7) 删除目录或者文件
"""
##############################################################
try:
	from hdfs import Client
	from hdfs.client import InsecureClient
except Exception as ex:
	print(ex)
from json import dump,dumps

class HdfsClient:
	"""基于hdfs library实现的hdfs客户端
	"""

	def __init__(self,host,port=50070):
		self.url = "http://%s:%d" % (host,port)
 		self.client = Client(url=self.url)
	
	def isExists(self,hdfs_path):
		try:
			status = self.client.acl_status(hdfs_path,strict=False)
			if status != None:
				info = "file or directory %s is existed." % hdfs_path
				return (0,info)
			else:
				info = "file or directory %s not existed." % hdfs_path
				return (1,info)
		except Exception,e:
			info="HDFS isExists:{}".format(str(e))
			return (2,info)
	def delete(self,hdfs_path,recursive=False):
		#Remove a file or directory from HDFS
		try:
			status = self.client.delete(hdfs_path,recursive=recursive)
			if status is True:
				info = "file or directory %s is deleted." % hdfs_path
				return (True,info)
			else:
				info = "file or directory %s failed to delete." % hdfs_path
				return (False,info)
		except Exception,e:
			info = "HDFS delete:{}".format(str(e))
			return (False,info)
	def write_data(self,hdfs_path,data):
		try:
			info = "write data to %s success" % hdfs_path
			self.client.write(hdfs_path,data=dumps(data),encoding='utf-8')
			return (True,info)
		except Exception as e:
			info = "HDFS write_data:{}".format(str(e))
			return (False,info)	
	
	def list_dirs(self,hdfs_path):
		"""list specific hdfs_path

		:Parameters:
			- 'hdfs_path': hdfs目录地址

		:Returns:
			包含指定目录下子文件名称的列表
		"""
		file_list = None
		try:
			info = "list %s success" % hdfs_path
			file_list = self.client.list(hdfs_path)
			return (file_list,info)
		except Exception as e:
			info = "list %s failed:%s" % (hdfs_path,str(e))
			return (file_list,info)

	def download(self,hdfs_path,local_path):
		"""download file from hdfs

			:Parametrs:
				- 'hdfs_path':下载文件所在路径
				- 'local_path': 下载文件待保存路径

			:Returns:
				True表示下载成功，False表示下载失败
		"""
		try:
			info = "download file from %s to %s" % (hdfs_path,local_path)
			self.client.download(hdfs_path,local_path,overwrite=True)
			return (True,info)
		except Exception as e:
			info = "HDFS download Failed:{}".format(str(e))
			return (False,info)

	def upload(self,hdfs_path,local_path):
		"""upload file from local to hdfs

		:Parameters:
			-'hdfs_path': 上传目标地址
			-'local_path': 本地上传文件地址

		:Returns：
			True上传成功,反之上传失败
		"""
		try:
			info = "HDFS upload file from %s to %s success" % (local_path,hdfs_path)
			self.client.upload(hdfs_path,local_path,overwrite=True)
			return (True,info)
		except Exception as e:
			info = "HDFS upload file from %s to %s failed:%s" % (local_path,hdfs_path,str(e))
			return (False,info)

	def mkdirs(self,dir_path,permission='0700'):
		"""make dir on specific path

		:Parameters：
			- 'dir_path':带创建目录,包含路径及目录名称
			- 'permission':目录权限
		"""
		try:
			info = "HDFS mkdirs success:{}".format(dir_path)
			self.client.makedirs(dir_path,permission=permission)
			return (True,info)
		except Exception as e:
			info = "HDFS mkdirs failed:{}:{}".format(dir_path,str(e))
			return (False,info)

	def rename(self,hdfs_src,hdfs_dst):
		"""重命名hdfs目录名称
		"""
		try:
			info = "HDFS rename %s to %s success" % (hdfs_src,hdfs_dst)
			self.client.rename(hdfs_src,hdfs_dst)
			return (True,info)
		except Exception as e:
			info = "HDFS rename %s to %s failed:%s" % (hdfs_src,hdfs_dst,str(e))
			return (False,info)
