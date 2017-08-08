#!/usr/bin/python
#!-*-coding:utf-8-*-
from lxml import etree
import datetime
import time
def parse_cpename(name):
	product={}
	product['name']=name
	ns=name[5:].split(':')
	try:
		product['part']=ns[0]
	except:
		product['part']=''
	try:
		product['vendor']=ns[1]
	except:
		product['vendor']=''
	try:
		product['product']=ns[2]
	except:
		product['product']=''
	try:
		product['version']=ns[3]
	except:
		product['version']=''
	try:
		product['update']=ns[4]
	except:
		product['update']=''
	try:
		product['edition']=ns[5]
	except:
		product['edition']=''
	try:
		product['language']=ns[6]
	except:
		product['language']=''
	try:
		product['sw_edition']=ns[7]
	except:
		product['sw_edition']=''
	try:
		product['target_sw']=ns[8]
	except:
		product['target_sw']=''
	try:
		product['target_hw']=ns[9]
	except:
		product['target_hw']=''
	try:
		product['other']=ns[10]
	except:
		product['other']=''
	return product
def parse_time(t):
	#2016-01-13T00:59:23.593-05:00
	tt=''.join(t.split('-')[:-1]).replace('T',' ')
	tt=tt.split('.')[:-1]
	tt=''.join(tt)
	ttt = time.strptime(tt, "%Y%m%d %H:%M:%S")
	ttt = datetime.datetime(*ttt[:6])
	return ttt
def init_cvss():
	cvss={}
	cvss['score']='0'
	cvss['access_vector']='unknown'
	cvss['access_complexity']='unknown'
	cvss['authentication']='unknown'
	cvss['confidentiality_impact']='unknown'
	cvss['integrity_impact']='unknown'
	cvss['availability_impact']='unknown'
	cvss['source']='unknown'
	cvss['generated_on_datetime']=datetime.datetime.now()
	return cvss
def init_reference():
	reference={}
	reference['source']=''
	reference['href']=''
	reference['text']=''
	reference['reference_type']=''
	return reference
def parse_cpe(flp="",NSMAP=None):
	doc=etree.parse(flp)
	cpe_items=doc.findall('.//mw:cpe-item',namespaces=NSMAP)
	for cpe_item in cpe_items:
		item={}
		item['storage_time']=datetime.datetime.now()
		name=cpe_item.xpath('@name',namespaces=NSMAP)[0]
		item['name']=name
		title=cpe_item.xpath('./mw:title[@xml:lang="en-US"]/text()',namespaces=NSMAP)
		item['title']=title
		references=[]
		refs=cpe_item.xpath('./mw:references/mw:reference',namespaces=NSMAP)
		if len(refs)>0:
			for ref in refs:
				reference={}
				reference['href']=ref.xpath('./@href')[0]
				reference['desc']=ref.xpath('./text()')[0]
				references.append(reference)
		item['references']=references
		name1=cpe_item.xpath('./cpe-23:cpe23-item/@name',namespaces=NSMAP)[0]
		name1=parse_cpename(name1.replace('2.3:','/'))
		item['details']=name1
		yield item
def parse_nvdcve(flp="",NSMAP=None):
	doc=etree.parse(flp)
	entrys=doc.findall('.//mw:entry',namespaces=NSMAP)
	for entry in entrys:
		vul={}
		vul['storage_time']=datetime.datetime.now()
		cve_id = entry.xpath('@id')[0]
		vul['cve_id']=cve_id
		vul['fact_refs']=[]
		cpe_vulconfs=entry.xpath('./vuln:vulnerable-configuration',namespaces=NSMAP)
		for cpe_vulconf in cpe_vulconfs:
			cpe_langs=cpe_vulconf.xpath('./cpe-lang:logical-test',namespaces=NSMAP)
			fact_refs={'operator':'','logical_test1':[],'logical_test2':[]}
			if len(cpe_langs)>0:
				if cpe_langs[0].xpath('@operator')[0]=="OR":
					cpe_langs=cpe_langs[0].xpath('./cpe-lang:fact-ref',namespaces=NSMAP)
					fact_refs['operator']="OR"
					for cpe_lang in cpe_langs:
						name=cpe_lang.xpath('@name')[0]
						product=parse_cpename(name)
						fact_refs['logical_test1'].append(product)
				else:
					logical_tests=cpe_langs[0].xpath('./cpe-lang:logical-test',namespaces=NSMAP)
					if len(logical_tests)>0:
						cpe_langs=logical_tests[0].xpath('./cpe-lang:fact-ref',namespaces=NSMAP)
						fact_refs['operator']="AND"
						for cpe_lang in cpe_langs:
							name=cpe_lang.xpath('@name')[0]
							product=parse_cpename(name)
							fact_refs['logical_test1'].append(product)
						cpe_langs=logical_tests[1].xpath('./cpe-lang:fact-ref',namespaces=NSMAP)
						for cpe_lang in cpe_langs:
							name=cpe_lang.xpath('@name')[0]
							product=parse_cpename(name)
							fact_refs['logical_test2'].append(product)
					else:
						fact_refs['operator']="AND"
						cpe_langs=cpe_langs[0].xpath('./cpe-lang:fact-ref',namespaces=NSMAP)
						for cpe_lang in cpe_langs:
							name=cpe_lang.xpath('@name')[0]
							product=parse_cpename(name)
							fact_refs['logical_test1'].append(product)
			else:
				print cpe_langs
			vul['fact_refs'].append(fact_refs)
		products=entry.xpath('./vuln:vulnerable-software-list/vuln:product',namespaces=NSMAP)
		vul['products']=[]
		if len(products) > 0:
			for product in products:
				name = product.xpath('text()')[0]
				pro = parse_cpename(name)
				vul['products'].append(pro)
		else:
			print products
		#vuln:published-datetime
		publish_dates=entry.xpath('./vuln:published-datetime',namespaces=NSMAP)
		#print "PUBLISH_TIME:"
		vul['publish_date']=datetime.datetime.now()
		if len(publish_dates)>0:
			publish_date=publish_dates[0].xpath('./text()')[0]
			vul['publish_date']=parse_time(publish_date)
		else:
			print publish_dates
		#<vuln:last-modified-datetime>2016-03-09T14:10:15.540-05:00</vuln:last-modified-datetime>
		update_times=entry.xpath('./vuln:last-modified-datetime',namespaces=NSMAP)
		#print "UPDATE_TIMES:"
		vul['last_modified_datetime']=datetime.datetime.now()
		if len(update_times)>0:
			last_modified_datetime=update_times[0].xpath('./text()')[0]
			vul['last_modified_datetime']=parse_time(last_modified_datetime)
		else:
			print update_times
		cvss=init_cvss()
		if len(entry.xpath('./vuln:cvss',namespaces=NSMAP)) > 0:
			scores=entry.xpath('./vuln:cvss/cvss:base_metrics/cvss:score/text()',namespaces=NSMAP)
			if len(scores)>0:
				cvss['score']=scores[0]
			access_vectors=entry.xpath('./vuln:cvss/cvss:base_metrics/cvss:access-vector/text()',namespaces=NSMAP)
			if len(access_vectors)>0:
				cvss['access_vector']=access_vectors[0]
			access_complexitys=entry.xpath('./vuln:cvss/cvss:base_metrics/cvss:access-complexity/text()',namespaces=NSMAP)
			if len(access_complexitys)>0:
				cvss['access_complexity']=access_complexitys[0]
		
			authentications=entry.xpath('./vuln:cvss/cvss:base_metrics/cvss:authentication/text()',namespaces=NSMAP)
			if len(authentications)>0:
				cvss['authentication']=authentications[0]
		
			confidentiality_impacts=entry.xpath('./vuln:cvss/cvss:base_metrics/cvss:confidentiality-impact/text()',namespaces=NSMAP)
			if len(confidentiality_impacts)>0:
				cvss['confidentiality_impact']=confidentiality_impacts[0]
			integrity_impacts=entry.xpath('./vuln:cvss/cvss:base_metrics/cvss:integrity-impact/text()',namespaces=NSMAP)
			if len(integrity_impacts)>0:
				cvss['integrity_impact']=integrity_impacts[0]
			availability_impacts=entry.xpath('./vuln:cvss/cvss:base_metrics/cvss:availability-impact/text()',namespaces=NSMAP)
			if len(availability_impacts)>0:
				cvss['availability_impact']=availability_impacts[0]
			sources=entry.xpath('./vuln:cvss/cvss:base_metrics/cvss:source/text()',namespaces=NSMAP)
			if len(sources)>0:
				cvss['source']=sources[0]
			generated_on_datetimes=entry.xpath('./vuln:cvss/cvss:base_metrics/cvss:generated-on-datetime/text()',namespaces=NSMAP)
			if len(generated_on_datetimes)>0:
				cvss['generated_on_datetime']=parse_time(generated_on_datetimes[0])
		else:
			print entry.xpath('./vuln:cvss',namespaces=NSMAP)
		vul['cvss']=cvss
		if len(entry.xpath('./vuln:cwe/@id',namespaces=NSMAP)) < 1:
			cwe_id=''
		else:
			cwe_id=entry.xpath('./vuln:cwe/@id',namespaces=NSMAP)[0]
		vul['cwe_id'] = cwe_id
		references=entry.xpath('./vuln:references[@xml:lang="en"]',namespaces=NSMAP)
		vul['references']=[]
		if len(references)>0:
			for reference in references:
				referencedict=init_reference()
				if len(reference.xpath('@reference_type',namespaces=NSMAP))>0:
					referencedict['reference_type']=reference.xpath('@reference_type',namespaces=NSMAP)[0]

				if len(reference.xpath('./vuln:source/text()',namespaces=NSMAP))>0:
					referencedict['source']=reference.xpath('./vuln:source/text()',namespaces=NSMAP)[0]
				else:
					print reference.xpath('./vuln:source/text()',namespaces=NSMAP)
				if len(reference.xpath('./vuln:reference/@href',namespaces=NSMAP))>0:
					referencedict['href']=reference.xpath('./vuln:reference/@href',namespaces=NSMAP)[0]
				else:
					print reference.xpath('./vuln:reference/@href',namespaces=NSMAP)
				if len(reference.xpath('./vuln:reference/text()',namespaces=NSMAP))>0:
					referencedict['text']=reference.xpath('./vuln:reference/text()',namespaces=NSMAP)[0]
				else:
					print reference.xpath('./vuln:reference/text()',namespaces=NSMAP)
				#print source,href,text
				vul['references'].append(referencedict)
		else:
			print references
		vul['summary']=''
		summarys=entry.xpath('./vuln:summary/text()',namespaces=NSMAP)
		if len(summarys)>0:
			vul['summary'] = summarys[0]
		else:
			print summarys
		yield vul
def getroot(filepath):
	tree = etree.parse(filepath)
	root = tree.getroot()
	nsmap = root.nsmap
	nsmap["default"] = nsmap[None]
	nsmap.pop(None)
	return (root,nsmap)
def parse_cve(item,nsmap):
	cve_item = dict()
	try:
		cve_item["type"] = item.get("type")
		cve_item["cve_id"] = item.get("name")
		cve_item['storage_time']=datetime.datetime.now()
		item_status = item.xpath("./default:status",namespaces=nsmap)[0]
		cve_item["status"] = item_status.text
		item_phase = dict()
		cve_item_phase = item.xpath("./default:phase",namespaces=nsmap)
		if len(cve_item_phase) > 0:
			item_phase["value"] = cve_item_phase[0].text
			item_phase["date"] = cve_item_phase[0].get("date")
		else:
			pass
		cve_item["phase"] = item_phase
		cve_item["desc"] = item.xpath("./default:desc",namespaces=nsmap)[0].text
		item_refs = item.xpath("./default:refs",namespaces=nsmap)[0]
		cve_refs = list()
		for item_ref in item_refs:
			cve_ref = dict()
			cve_ref["ref"] = item_ref.text
			if item_ref.get('url'):
				cve_ref['url'] = item_ref.get('url')
			else:
				cve_ref['url'] = ''
			cve_ref["source"] = item_ref.get("source")
			cve_refs.append(cve_ref)
		item_votes = item.xpath("./default:votes",namespaces=nsmap)
		cve_item["votes"] = {"accept":"","modify":"","noop":"","recast":"","reject":"","reviewing":"","revote":""}
		if len(item_votes) > 0:
			item_votes = item_votes[0]
			item_vote_list = item_votes.xpath("./default:*",namespaces=nsmap)
			for item_vote in item_vote_list:
				cve_item["votes"][item_vote.tag.split("}")[1]] = item_vote.text
		else:
			pass
		item_comments = item.xpath("./default:comments",namespaces=nsmap)
		cve_item["comments"] = list()
		if len(item_comments) > 0:
			item_comments = item_comments[0]
			item_comment_list = item_comments.xpath("./default:comment",namespaces=nsmap)
			for item_comment in item_comment_list:
				comment = dict()
				comment["comment"] = item_comment.text
				comment["voter"] = item_comment.get("voter")
				cve_item["comments"].append(comment)
		else:
			pass
		cve_item["refs"] = cve_refs
		print cve_item
		return (cve_item,"Parse success")
	except Exception,e:
		return (None,str(e))	
def parse_all_cve(filepath):
	(root,nsmap)=getroot(filepath)
	item_list = root.xpath("./default:item",namespaces=nsmap)
	for item in item_list:
		cve_item,info=parse_cve(item,nsmap)
		print cve_item,info
		yield cve_item
