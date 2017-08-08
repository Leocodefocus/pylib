#!/usr/bin/python
#!-*-coding:UTF-8-*-
import requests
from bs4 import BeautifulSoup
import re
import threading
import datetime
import time
import pymongo
import urlparse
import sys
import os
import random
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
def initialfunc():
		item = {}
		item['name']=[]
		item['vul_id']=""
		item['authentication']=""
		item['confidentiality_impact']=""
		item['reference']=[]
		item['link']=""
		item['reference_id']=[]
		item['gained_acess']=""
		item['availability_impact']=""
		item['level']=""
		item['description']=[]
		item['vul_class']=""
		item['vul_type']=[]
		item['vul_hash']=""
		item['status']=""
		item['products']=[]
		item['found_time']=""
		item['publish_time']=""
		item['commit_time']=""
		item['threat_type']=""
		item['vul_supply']=""
		item['vul_founder']=""
		item['solution']=""
		item['exploit']=[]
		item['fix']=[]
		item['integrity_impact']=""
		item['access_complexity']=""
		item['cvss_score']=""
		item['source']=[]
		item['create_user']=""
		item['create_time']=""
		item['update_user']=""
		item['update_time']=""
		item['op_type']=""
		return item
def parseVul(url,html):
		item = initialfunc()
		item['link'] = url
		bsObj = BeautifulSoup(html)
		try:
			tds = bsObj.find("td",text="漏洞名称：").next_siblings
			for td in tds:
				try:
					item["name"] = td.get_text()
				except Exception,e:
					print "Error"
		except AttributeError:
			print "Error"
		tds = bsObj.find("td",text="CNNVD编号：".decode("UTF-8")).next_siblings
		for td in tds:
			try:
				item['source_id'] = td.get_text()
			except:
				pass
		#发布时间：
		try:
			tds = bsObj.find("td",text="发布时间：".decode("UTF-8")).next_siblings
			for td in tds:
				try:
					item['publish_time'] = td.get_text()
				except:
					pass
		except AttributeError:
			pass
		item['publish_time']=parseTime(item['publish_time'].strip())
		item['update_time']=datetime.datetime.now()
		item['commiit_time']=datetime.datetime.now()
		item['found_time']=datetime.datetime.now()
		try:
			tds = bsObj.find("td",text="漏洞类型：".decode("UTF-8")).next_siblings
			for td in tds:
				try:
					item['vul_type'] = td.a.get_text()
				except:
					pass
		except AttributeError:
			pass
		try:
			tds = bsObj.find("td",text="威胁类型：".decode("UTF-8")).next_siblings
			for td in tds:
				try:
					item['threat_type'] = td.a.get_text()
				except:
					pass
		except AttributeError:
			pass
		try:
			tds = bsObj.find("td",text="CVE编号：".decode("UTF-8")).next_siblings
			for td in tds:
				try:
					item['reference_id'].append(td.a.get_text())
				except:
					pass
		except AttributeError:
			pass
		try:
			tds = bsObj.find("td",text="漏洞来源：".decode("UTF-8")).next_siblings
			for td in tds:
				try:
					item['vendor']=td.get_text()
				except:
					pass
		except AttributeError:
			pass
		#description
		description = bsObj.find("div",{"class":"container"}).find("div").table.find("tr").table.find("tr").next_sibling.next_sibling
		all_ps = description.find("div",{"class":"cont_details"}).findAll("p")
		des = ""
		for p in all_ps:
			try:
				des += p.get_text()
			except:
				pass
		item['description'].append(des)
		#fix
		fixs = description.next_sibling.next_sibling
		a_hrefs = fixs.find("div",{"class":"cont_details"}).find("p").findAll("a")
		for a_href in a_hrefs:
			if "href" in a_href.attrs:
				item['fix'].append(a_href['href'])
		#reference
		references = fixs.next_sibling.next_sibling
		a_hrefs = references.td.find("div",{"class":"cont_details1"}).findAll("a")
		for a_href in a_hrefs:
			if "href" in a_href.attrs:
				item["reference"].append(a_href['href'])

		#source
		s={}
		s["source"]="CNNVD"
		s["link"]=response.url
		s["id"]=item['source_id']
		item['source'].append(s)
		return item
def dbHandler(collection):
		connection=pymongo.MongoClient(
			dbconfig.MONGODB_SERVER,
			dbconfig.MONGODB_PORT
			)
		db=connection[dbconfig.MONGODB_DB]
		conn=db[collection]
		return conn
