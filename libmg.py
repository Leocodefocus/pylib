#!/usr/bin/python
#!-*-coding:utf-8-*-
import pymongo
class mgpack:
	def __init__(self,server,port):
		self.server = server
		self.port = port
		self.connection = None
		self.db = None
	def conn_mgClient(self):
		try:
			self.connection=pymongo.MongoClient(
				self.server,
				self.port
				)
			info = "Mongodb conn_mgClient:success"
			return (1,info)
		except Exception,e:
			self.connection=None
			info="Mongodb conn_mgClient:{}".format(str(e))
			return (0,info)
	def conn_db(self,db):
		if self.connection != None:
			try:
				self.db = self.connection[db]
				info = "Mongodb conn_db:success"
				return (1,info)
			except Exception,e:
				info = "Mongodb conn_db:{}".format(str(e))
				return (0,info)
		else:
			info="Mongodb conn_db:Please connect MongodbClient first!"
			self.db = None
			return (0,info)
	def conn_collection(self,collection):
		if self.db != None:
			try:
				conn = self.db[collection]
				info = "Mongodb conn_collection:success"
				return (conn,info)
			except Exception,e:
				info = "Mongodb conn_collection:{}".format(str(e))
				return (None,info)
		else:
			info = "Mongodb conn_collection:Please connect db first!"
			return (None,info)
	def db_searchAll(self,conn,no_cursor_timeout=True):
		items=None
		info = None
		try:
			items = conn.find(no_cursor_timeout=no_cursor_timeout)
			info = "Mongodb db_searchAll:success"
		except Exception,e:
			info="Mongodb db_searchAll:{}".format(str(e))
		return (items,info)
	def db_searchDate(self,conn,field,preT,curT,no_cursor_timeout=False):
		items=None
		info = None
		query = {field:{"$gt":preT,"$lt":curT}}
		try:
			items = conn.find(filter=query,no_cursor_timeout=no_cursor_timeout)
			info = "Mongodb db_searchDate:success"
		except Exception,e:
			info = "Mongodb db_searchDate:{}".format(str(e))
		return (items,info)
	def db_searchFilter(self,conn,dbFilter,no_cursor_timeout=False):
		items=None
		info = None
		try:
			items = conn.find(filter=dbFilter,no_cursor_timeout=no_cursor_timeout)
			info = "Mongodb db_searchFilter:success"
		except Exception,e:
			info = "Mongodb db_searchFilter:{}".format(str(e))
		return (items,info)
	def db_remove(self,conn,dbFilter):
		try:
			conn.remove(dbFilter)
			info = "Mongodb db_remove:success"
			return (1,info)
		except Exception,e:
			info = "Mongodb db_remove:{}".format(str(e))
			return (0,info)
	def db_insert(self,conn,item,rmdup=False,query=None):
		try:
			if rmdup == False:
				conn.insert(item)
				info = "Mongodb db_insert(),rmdup=False,item no ideas"
				return (1,info)
			else:
				num = conn.find(query).count()
				if num < 1:
					conn.insert(item)
					info = "Mongodb db_insert(),rmdup=True,item is not existed {}".format(str(num))
					return (1,info)
				else:
					info = "Mongodb db_insert(),rmdup=True,item has existed {}".format(str(num))
					return (1,info)
		except Exception,e:
			info = "Mongodb db_insert:{}".format(str(e))
			return (0,info)
	def db_modify(self,conn,item,query=None):
		try:
			dbFilter=query
			(items,info)=self.db_searchFilter(conn,dbFilter,no_cursor_timeout=True)
			if items != None:
				(status,info)=self.db_remove(conn,dbFilter)
				if not status:
					return (status,info)
			else:
				return (0,info)
			(status,info) = self.db_insert(conn,item,rmdup=False,query=None)
			if status:
				return (status,"Mongodb db_modify:success")
			else:
				return (0,info)
		except Exception,e:
			info = "Mongodb db_modify:{}".format(str(e))
			return (0,info)
