#!-*-coding:utf-8-*-
import sys
sys.path.append(r'/root/move')
import datetime
from elasticsearch import helpers
from bson.objectid import ObjectId
import elasticsearch
from elasticsearch import Elasticsearch
import pymongo
import threading
import time
import datetime
from libs.libmg import mgpack
from libs import configpara
from libs.liblog import selflog
import libs.configdb as dbconfig
from libs.libtime import trans_cur
from libs import configes as esconfig
from libs.libes import espack
login_dict = {'host':[ip],'port':9200}
tstr=trans_cur()
myLogger = selflog('{}/{}.log'.format(configpara.DATAUP_LOG_PATH,tstr)).getLogger()

#database tables or collections 
collections = [
		dbconfig.MONGODB_COLLECTION_1,
		dbconfig.MONGODB_COLLECTION_2,
		dbconfig.MONGODB_COLLECTION_3,
		dbconfig.MONGODB_COLLECTION_4,
		dbconfig.MONGODB_COLLECTION_5,
		dbconfig.MONGODB_COLLECTION_6,
		dbconfig.MONGODB_COLLECTION_7,
		dbconfig.MONGODB_COLLECTION_8,
		dbconfig.MONGODB_COLLECTION_9,
		dbconfig.MONGODB_COLLECTION_10,
		dbconfig.MONGODB_COLLECTION_11,
		dbconfig.MONGODB_COLLECTION_12,
		dbconfig.MONGODB_COLLECTION_13,
		dbconfig.MONGODB_COLLECTION_VULNERABILITY,
	]
mappings = {
				dbconfig.MONGODB_COLLECTION_1:esconfig.1_MAPPING,
				dbconfig.MONGODB_COLLECTION_2:esconfig.2_MAPPING,
				dbconfig.MONGODB_COLLECTION_3:esconfig.3_MAPPING,
				dbconfig.MONGODB_COLLECTION_4:esconfig.4_MAPPING,
				dbconfig.MONGODB_COLLECTION_5:esconfig.5_MAPPING,
				dbconfig.MONGODB_COLLECTION_6:esconfig.6_MAPPING,
				dbconfig.MONGODB_COLLECTION_7:esconfig.7_MAPPING,
				dbconfig.MONGODB_COLLECTION_8:esconfig.8_MAPPING,
				dbconfig.MONGODB_COLLECTION_9:esconfig.9_MAPPING,
				dbconfig.MONGODB_COLLECTION_10:esconfig.10_MAPPING,
				dbconfig.MONGODB_COLLECTION_11:esconfig.11_MAPPING,
				dbconfig.MONGODB_COLLECTION_12:esconfig.12_MAPPING,
				dbconfig.MONGODB_COLLECTION_13:esconfig.14_MAPPING,
				dbconfig.MONGODB_COLLECTION_VULNERABILITY:esconfig.VULNERABILITY_MAPPING,
			}
#login ES client
def es_login(login_dict):
	try:
		es = Elasticsearch([login_dict])
		return es
	except elasticsearch.ElastisearchException,e:
		myLogger.debug(str(e))
		return None

#Create index in es
def create_index(es,myindex):
	if not es.indices.exists(myindex):
		create_result = es.indices.create(index=myindex,ignore=400)
		myLogger.info("ES [{}] index has created.".format(myindex))
	else:
		myLogger.info("ES [{}] index has existed.".format(myindex))

#Connect to Mongodb Norn
def conn_db(dbstr):
	try:
		mgdb=mgpack(dbconfig.MONGODB_SERVER,dbconfig.MONGODB_PORT)
		(status,info)=mgdb.conn_mgClient()
		if status:
			myLogger.info(info)
		else:
			myLogger.debug(info)
			exit(0)
		(status,info)=mgdb.conn_db(dbstr)
		if status:
			myLogger.info(info)
		else:
			myLogger.debug(info)
			exit(0)
		myLogger.info("conn_db success to connect:[{}]>[{}]>[{}]".format(dbconfig.MONGODB_SERVER,dbconfig.MONGODB_PORT,dbstr))
		return mgdb
	except Exception,e:
		myLogger.debug("conn_db failed to connect:[{}]>[{}]>[{}]".format(dbconfig.MONGODB_SERVER,dbconfig.MONGODB_PORT,dbstr))
		return None
#insert items to es by doc_type
def insert_items(es,index,conn,doc_type):
	count = conn.find(no_cursor_timeout=True).count()
	print count
	items = conn.find(no_cursor_timeout=True)
	i=1
	actions = []
	print "{}:{}".format(index,doc_type)
	for item in items:
		oid = str(item['_id'])
		item.pop('_id')
		item['oid'] = oid
		print "{}:{}...{}".format(index,doc_type,oid)
		if "op_type" in item.keys():
			item.pop('op_type')
		if "update_user" in item.keys():
			item.pop('update_user')
		if "create_user" in item.keys():
			item.pop('create_user')
		if "vendor_id" in item.keys():
			item['vendor_id']=str(item['vendor_id'])
		action={
			"_index":index,
			"_type":doc_type,
			"_id":i,
			"_source":item
		}
		i+=1
		actions.append(action)
		if (len(actions)==2000):
			helpers.bulk(es,actions)
			del actions[0:len(actions)]
	if (len(actions)>0):
		helpers.bulk(es,actions)
		'''body={
			"query":{
				"match":{
					"oid":item['oid'],
				}
			}
		}
		num = es.count(index=index,doc_type=doc_type,body=body)
		print num['count']
		if num['count'] > 0:
			myLogger.info("index={},doc_type={},number={} has existed.".format(index,doc_type,str(i)))
		else:
			try:
				result = es.index(index=index,doc_type=doc_type,body=item)
				myLogger.info("index={},doc_type={},number={} stored".format(index,doc_type,str(i)))
			except Exception,e:
				myLogger.info("index={},doc_type={},number={} ERROR:[{}]".format(index,doc_type,str(item['oid']),str(e)))'''

#Modify or Update or add mappings for ES index
def update_mapping(es,index,doctype,mapp):
	es.indices.put_mapping(index=index,doc_type=doctype,body=mapp,update_all_types=True)
def delete_data(login_dict):
	print login_dict
	esp=espack(login_dict)
	print "Login.."
	esp.es_login(login_dict)
	print "Success"
	esp.deleteEsDoc(dbconfig.MONGODB_DB,dbconfig.MONGODB_COLLECTION_1)
	print "DELETE..."
def bulk_upload():
	es = es_login(login_dict)
	db = conn_db(dbconfig.MONGODB_DB_1)
def main():
	es = es_login(login_dict)
	index="norn"
	create_index(es,index)
	db = conn_db(dbconfig.MONGODB_DB_1)
	for collection in collections:
		doc = collection
		(conn,info) = db.conn_collection(collection)
		if conn != None:
			myLogger.info(info)
			mapps = mappings[doc]
			myLogger.info("Start update mapping and inisert items to [{}]".format(doc))
			update_mapping(es,index,doc,mapps)
			t = threading.Thread(target=insert_items,args=(es,index,conn,doc))
			t.start()
		else:
			myLogger.debug(info)
if __name__=='__main__':
	main()
