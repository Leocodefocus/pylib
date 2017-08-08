#!-*-coding:utf-8-*-
import datetime
from elasticsearch import helpers
from bson.objectid import ObjectId
import elasticsearch
from elasticsearch import Elasticsearch
from liblog import selflog
import time

class espack:
	def __init__(self,login_dict):
		self.login_dict=login_dict
		self.es=None
		mm = selflog("es.log")
		self.myLogger=mm.getLogger()
	#login ES client
	def es_login(self,login_dict):
		try:
			self.es = Elasticsearch([login_dict])
			#return es
		except Exception,e:
			self.myLogger.debug(str(e))
			self.es=None
			#return None
	#Create index in es
	def create_index(self,myindex):
		if self.es != None:
			if not es.indices.exists(myindex):
				create_result = es.indices.create(index=myindex,ignore=400)
		else:
			self.myLogger.info("Please login in es first!")
	#search items by query body in ES
	def search_items(self,index,doc_type,body):
		try:
			results = helpers.scan(self.es,query=body,scroll="10000m",index=index,doc_type=doc_type,request_timeout=30)
			return results
		except Exception,e:
			self.myLogger.debug(str(e))
			return None
	#delete item by id in ES
	def delete_item(self,index,doc_type,D_id):
		#es = es_login(login_dict)
		try:
			self.es.delete(index=index,doc_type=doc_type,id=D_id,refresh="true")
		except Exception,e:
			self.myLogger.debug(str(e))
	#delete items through pass items	
	def delete_items(self,index,doc_type,results):
		#es = es_login(login_dict)
		print "DELETE items.."
		try:
			print "executes"
			for result in results:
				print result['_id']
				self.delete_item(index,doc_type,result['_id'])
		except Exception,e:
			print str(e)
			self.myLogger.debug(str(e))
	#update item in es by id
	def es_update_item(self,index,doc_type,D_id,body):
		try:
			self.es.update(index=index,doc_type=doc_type,id=D_id,body=body,refresh="true")
		except Exception,e:
			self.myLogger.debug(str(e))
	#insert items to es by doc_type
	def insert_items(self,index,items,doc_type):
		#count = conn.find(no_cursor_timeout=True).count()
		#print count
		#items = conn.find(no_cursor_timeout=True)
		i=1
		print "{}:{}".format(index,doc_type)
		for item in items:
			oid = str(item['_id'])
			item.pop('_id')
			item['oid'] = oid
			print "{}:{}...{}".format(index,doc_type,oid)
			if "op_type" in item.keys():
				item.pop('op_type')
			body={
				"query":{
					"match":{
						"oid":item['oid'],
					}
				}
			}
			num = self.es.count(index=index,doc_type=doc_type,body=body)
			print num['count']
			if num['count'] > 0:
				myLogger.info("index={},doc_type={},number={} has existed.".format(index,doc_type,str(i)))
			else:
				result = self.es.index(index=index,doc_type=doc_type,body=item)
				myLogger.info("index={},doc_type={},number={} stored".format(index,doc_type,str(i)))
			i+=1
	#insert item to es alone
	def insert_item_only(self,index,doc_type,item):
		try:
			self.es.index(index=index,doc_type=doc_type,body=item)
		except Exception,e:
			self.myLogger.error("{}:{}".format(doctype,str(e)))
			exit(0)
	#reset index
	def resetIndex(index):
		#es = es_login(login_dict)
		self.es.indices.delete(index)
		self.create_index(index)
	def deleteEsDoc(self,index,doc_type):
		body = {
			"query":{"match_all":{}}
		}
		results = self.search_items(index,doc_type,body)
		print results
		self.delete_items(index,doc_type,results)
