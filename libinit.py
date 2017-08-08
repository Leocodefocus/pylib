#!/usr/bin/python
#!-*-coding:utf-8-*-
def init_cve():
    item={}
    item['vul_id']=''
    item['type']=''
class logs:
    def __init__(self):
        self.logs = {}
        self.init_log()
        self.sql_ = "insert into actionlogs(ymdtime,vulname,action,starttime,endtime,ps,exception,excpinfo) values('{}','{}','{}','{}','{}','{}','{}','{}')"
    def init_log(self):
        self.logs['ymdtime'] = ''
        self.logs['vulname'] = ''
        self.logs["action"] = ''
        self.logs['starttime'] = ''
        self.logs['endtime'] = ''
        self.logs['ps'] = ''
        self.logs['exception'] = ''
        self.logs['excpinfo'] = ''
    def set_log(self,time,vulname,action,starttime,endtime,ps,exception,excpinfo):
        self.logs['ymdtime'] = time
        self.logs['vulname'] = vulname
        self.logs["action"] = action
        self.logs['starttime'] = starttime
        self.logs['endtime'] = endtime
        self.logs['ps'] = ps
        self.logs['exception'] = exception
        self.logs['excpinfo'] = excpinfo
    def get_sql(self):
        sql_cent = self.sql_.format(self.logs['ymdtime'].replace("'","\""),self.logs['vulname'].replace("'","\""),self.logs['action'].replace("'","\""),self.logs['starttime'].replace("'","\""),self.logs['endtime'].replace("'","\""),self.logs['ps'].replace("'","\""),self.logs['exception'].replace("'","\""),self.logs['excpinfo'].replace("'","\""))
        return sql_cent
class nvd_sql():
    def __init__(self):
        self.vuln_insert = "insert into vuln_nvd(cve_id,vuln_desc,vuln_score,cwe_id,last_modified_time,published_time,nvd_url,create_user,create_time,update_user,update_time) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
        self.vuln_cvss = "insert into vuln_nvd_cvss(cve_id,score,av_en,ac_en,au_en,c_en,i_en,a_en,source,generated_on_time,create_user,create_time)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
        self.vuln_refer = "insert into vuln_nvd_refer(cve_id,refer_type,source,content,link,create_user,create_time)values('%s','%s','%s','%s','%s','%s','%s')"
        self.vuln_tag = "insert into vuln_nvd_tag(cve_id,tag_id,create_user,create_time)values('%s','%s','%s','%s')"