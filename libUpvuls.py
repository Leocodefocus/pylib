#!/usr/bin/python
# !-*-coding:utf-8-*-
'''
    Author:leo
    Date:2017/06/12
    Description将NVD漏洞信息存储到Mysql数据库中，Vuln_nvd,vuln_nvd_cvss,patch,refer,tag...
    Note:SQL语句书写注意字符串中的单引号、反斜杠的转义
'''
import datetime
import sys
from libtime import parseTime
from libtime import get_localtime_str
reload(sys)
sys.setdefaultencoding('utf-8')


class upNvdSql:
    def __init__(self, conn_my, cursor):
        self.vuln_insert = "insert into vuln_nvd(cve_id,vuln_desc,vuln_score,cwe_id,last_modified_time,published_time,nvd_url,create_user,create_time,update_user,update_time) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
        self.vuln_cvss = "insert into vuln_nvd_cvss(cve_id,score,av_en,ac_en,au_en,c_en,i_en,a_en,source,generated_on_time,create_user,create_time)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
        self.vuln_refer = "insert into vuln_nvd_refer(cve_id,refer_type,source,content,link,create_user,create_time)values('%s','%s','%s','%s','%s','%s','%s')"
        self.vuln_tag = "insert into vuln_nvd_tag(cve_id,tag_id,create_user,create_time)values('%s','%s','%s','%s')"
        self.search_tag = "select * from vuln_cnvd where cve_id = '{}'"
        self.conn_my = conn_my
        self.cursor = cursor

    def upnvd(self, item):
        t_str = datetime.datetime.now().strftime('%Y-%m-%d')
        last_modified_time = item['last_modified_datetime'].strftime('%Y-%m-%d')
        published_time = item['publish_date'].strftime('%Y-%m-%d')
        nvd_base_url = "https://nvd.nist.gov/vuln/detail/"
        nvd_url = nvd_base_url + item['cve_id']
        create_user = '1'
        create_time = t_str
        update_user = '1'
        update_time = t_str
        if not item['cvss']['score']:
            item['cvss']['score'] = '0'
        print item['cvss']['score']
        vuln_sent = self.vuln_insert % (
        item['cve_id'], item['summary'].replace('\'', '"').replace('\\', '/'), item['cvss']['score'], item['cwe_id'],
        last_modified_time, published_time, nvd_url, create_user, create_time, update_user, update_time)
        print "INSERT:", vuln_sent.encode('utf-8')
        self.cursor.execute(vuln_sent.encode('utf-8'))
        self.conn_my.commit()

        generated_on_datetime = item['cvss']['generated_on_datetime'].strftime('%Y-%m-%d')
        vuln_cvss_sent = self.vuln_cvss % (
        item['cve_id'], item['cvss']['score'], item['cvss']['availability_impact'], item['cvss']['access_complexity'],
        item['cvss']['authentication'], item['cvss']['confidentiality_impact'], item['cvss']['integrity_impact'],
        item['cvss']['access_vector'], item['cvss']['source'].replace('\'', '"').replace('\\', '/'),
        generated_on_datetime, create_user, create_time)
        print "INSERT:", vuln_cvss_sent.encode('utf-8')
        self.cursor.execute(vuln_cvss_sent.encode('utf-8'))
        self.conn_my.commit()
        # vuln_refer = "insert into vuln_nvd_refer(cve_id,refer_type,source,content,link,create_user,create_time)values('%s','%s','%s','%s','%s','%s','%s')"
        for reference in item['references']:
            vuln_refer_sent = self.vuln_refer % (
            item['cve_id'], reference['reference_type'], reference['source'].replace('\'', '"').replace('\\', '/'),
            reference['text'].replace('\'', '"').replace('\\', '/'),
            reference['href'].replace('\'', '"').replace('\\', '/'), create_user, create_time)
            print "INSERT:", vuln_refer_sent.encode('utf-8')
            self.cursor.execute(vuln_refer_sent.encode('utf-8'))
            self.conn_my.commit()

        '''if conn_cnvd.find({'cve_id':item['cve_id'],'industry_type':'ics'}).count()>0:
            vuln_tag_sent = self.vuln_tag%(item['cve_id'],'9','1',create_time)
            print "INSERT:",vuln_tag_sent.encode('utf-8')
            cursor.execute(vuln_tag_sent.encode('utf-8'))
            conn_my.commit()'''


class upCveSql:
    def __init__(self, conn_cve):
        self.vuln_cve = "insert into vuln_cve(cve_id,vuln_desc,vuln_type,vuln_status,phase_date,phase_value,state,create_user,create_time,update_user,update_time)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
        self.vuln_cve_comment = "insert into vuln_cve_comment(cve_id,content,voter,create_user,create_time)values('%s','%s','%s','%s','%s')"
        self.vuln_cve_refer = "insert into vuln_cve_refer(cve_id,refer_url,refer_source,refer_name,create_user,create_time)values('%s','%s','%s','%s','%s','%s')"
        self.vuln_cve_tag = "insert into vuln_cve_tag(cve_id,tag_id,create_user,create_time)values('%s','%s','%s','%s')"
        self.vuln_cve_vendor = "insert into vuln_cve_vendor(cve_id,vendor_id,create_user,create_time)values('%s','%s','%s','%s')"
        self.vuln_cve_votes = "insert into vuln_cve_votes(cve_id,recast,modify,accept,noop,reviewing,reject,revote,create_user,create_time)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
        self.search_cnvd = "select * from vuln_cnvd where cve_id='%s'"
        self.search_cve = "select * from vuln_cve where cve_id='%s'"
        self.search_votes = "select * from vuln_cve_votes where cve_id='%s'"
        self.conn_cve = conn_cve

    def upcve(self, item):
        try:
            t_str = datetime.datetime.now().strftime('%Y-%m-%d')
            search_sent = self.search_cve % (item['cve_id'])
            (status, result) = self.conn_cve.c_search(search_sent)
            if status:
                return (1, result)
            print "--------------------", result
            if result < 1:
                # 漏洞SQL插入
                print "........................"
                print len(item['phase'].keys())
                if len(item['phase'].keys()) < 1:
                    item['phase'] = {}
                    item['phase']['date'] = t_str
                    item['phase']['value'] = ''
                else:
                    if item['phase']['date'] == '':
                        item['phase']['date'] = t_str
                    else:
                        item['phase']['date'] = str(parseTime(item['phase']['date']))
                print item['phase']['date']
                print "--------------------------------"
                cve_sent = self.vuln_cve % (
                item['cve_id'], item['desc'].replace('\'', '"').replace('\\', '/'), item['type'], item['status'],
                item['phase']['date'], item['phase']['value'], '0', '1', t_str, '1', t_str)
                print cve_sent
                (status, result) = self.conn_cve.insert(cve_sent)
                if status:
                    print result
                    return (1, result)
                else:
                    print "success"
                # Comment字段SQL插入
                if len(item['comments']) > 0:
                    for comment in item['comments']:
                        if len(comment.keys()) > 0:
                            comment_sent = self.vuln_cve_comment % (
                                item['cve_id'], comment['comment'].replace('\'', '"').replace('\\', '/'),
                                comment['voter'], '1',
                                t_str)
                            (status, result) = self.conn_cve.insert(comment_sent)
                            if status:
                                return (1, result)
                            else:
                                pass
                # Refer字段插入vuln_cve_refer = "insert into vuln_cve_refer(cve_id,refer_url,refer_source,refer_name,create_user,create_time)values('%s','%s','%s','%s','%s','%s')"
                if len(item['refs']) > 0:
                    for reference in item['refs']:
                        if reference['url'] == '':
                            reference['url'] = 'empty'
                        refer_sent = self.vuln_cve_refer % (
                            item['cve_id'], reference['url'].replace('\'', '"').replace('\\', '/'), reference['source'],
                            reference['ref'].replace('\'', '"').replace('\\', '/'), '1', t_str)
                        (status, result) = self.conn_cve.insert(refer_sent)
                        if status:
                            return (1, result)
                        else:
                            pass
                # tag字段插入vuln_cve_tag = "insert into vuln_cve_tag(cve_id,tag_id,create_user,create_time)values('%s','%s','%s','%s')"
                # cnvd_sql = mysql_lib()
                # cnvd_sql.conn_db(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
                search_sent = self.search_cnvd % (item['cve_id'])
                (status, result) = self.conn_cve.c_search(search_sent)
                if status:
                    result(1, result)
                else:
                    if result < 1:
                        tag_sent = self.vuln_cve_tag % (item['cve_id'], '9', '1', t_str)
                        (status, result) = self.conn_cve.insert(tag_sent)
                        if status:
                            return (1, result)
                        else:
                            pass

                # votes字段插入vuln_cve_votes = "insert into vuln_cve_votes(cve_id,recast,modify,accept,noop,reviewing,reject,revote,create_user,create_time)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                search_sent = self.search_votes % (item['cve_id'])
                (status, result) = self.conn_cve.c_search(search_sent)
                if status:
                    result(1, result)
                else:
                    if result < 1:
                        for key in item['votes'].keys():
                            if item['votes'][key] == '':
                                item['votes'][key] == 'empty'
                        votes_sent = self.vuln_cve_votes % (
                            item['cve_id'], item['votes']['recast'], item['votes']['modify'], item['votes']['accept'],
                            item['votes']['noop'], item['votes']['reviewing'], item['votes']['reject'],
                            item['votes']['revote'], '1',
                            t_str)
                        print votes_sent
                        (status, result) = self.conn_cve.insert(votes_sent)
                        if status:
                            print "171", result
                            return (1, result)
                        else:
                            pass
            return (0, "success")
        except Exception, e:
            return (1, str(e))

class upSecurityFocus:
    def __init__(self,conn_sec):
        self.vuln_sec = "insert into vuln_securityfocus(bugtraq_id,vuln_name,vuln_class,vuln_remote,vuln_local,vuln_credit,published_time,updated_time,vuln_discussion,vuln_exploit,vuln_solution,bid_url,create_user,create_time,update_user,update_time)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
        self.vuln_sec_cve = "insert into vuln_securityfocus_cve(bid,cve_id,create_user,create_time)values('%s','%s','%s','%s')"
        self.vuln_sec_product = "insert into vuln_securityfocus_product(bid,product_version_id,vulnerable,content,create_user,create_time)values('%s','%s','%s','%s','%s','%s')"
        self.vuln_sec_refer = "insert into vuln_securityfocus_refer(bid,title,link,create_user,create_time)values('%s','%s','%s','%s','%s')"
        self.vuln_sec_tag = "insert into vuln_securityfocus_tag(bid,tag_id,create_user,create_time)values('%s','%s','%s','%s')"
        self.vuln_sec_vendor = "insert into vuln_securityficus_vendor(bid,vendor_id,create_user,create_time)values('%s','%s','%s','%s')"
        self.search_bug_id = "select * from vuln_securityfocus where bugtraq_id = '%s'"
        self.search_tag_id = "select * from vuln_securityfocus_tag where bid = '%s'"
        self.search_cnvd = "select cnvd_id from vuln_cnvd where cve_id='%s'"
        self.search_cnvd_tag = "select a.cnvd_id,b.tag_id from vuln_cnvd as a INNER JOIN vuln_cnvd_tag as b where a.cnvd_id = b.cnvd_id and b.tag_id='9' and a.cve_id='%s'"
        self.conn_sec = conn_sec
    def upsec(self,item):
        try:
            updated_time = item['updated_time'].strftime('%Y-%m-%d')
            published_time = item['published'].strftime('%Y-%m-%d')
            vuln_sec_sent = self.vuln_sec%(item['bugtraq_id'],item['name'].replace('\'','"').replace('\\','/'),item['Class'].replace('\'','"').replace('\\','/'),item['remote'],item['local'],item['credit'].replace('\'','"').replace('\\','/'),published_time,updated_time,item['discussion'].replace('\'','"').replace('\\','/'),item['exploit'].replace('\'','"').replace('\\','/'),item['solution'].replace('\'','"').replace('\\','/'),item['url'].replace('\'','"').replace('\\','/'),'1',get_localtime_str(),'1',get_localtime_str())
            search_sent = self.search_bug_id%(item['bugtraq_id'])
            (status,info) = self.conn_sec.c_search(search_sent)
            print "207:",info
            if status:
                return (status,info)
            if info<1:
                #Insert into vuln_securityfocus table
                print "Insert into vuln_securityfocus table"
                (status,info)=self.conn_sec.insert(vuln_sec_sent)
                if status:
                    return (status,info)
                #Insert into vuln_securityfocus_cve table
                print "Insert into vuln_securityfocus_cve table"
                tag = 0
                for cve_id in item['cve_id']:
                    vuln_cve_sent = self.vuln_sec_cve%(item['bugtraq_id'],cve_id,'1',get_localtime_str())
                    (status, info) = self.conn_sec.insert(vuln_cve_sent)
                    if status:
                        return (status, info)
                    search_tag_cent = self.search_cnvd_tag%(cve_id)
                    (status,info) = self.conn_sec.c_search(search_tag_cent)
                    if status:
                        return (status,info)
                    if not info:
                        tag = 1
                #Insert into vuln_securityfocus_refer table
                print "Insert into vuln_securityfocus_refer table"
                for refer in item['references']:
                    vuln_refer_sent = self.vuln_sec_refer%(item['bugtraq_id'],refer,'','1',get_localtime_str())
                    (status, info) = self.conn_sec.insert(vuln_refer_sent)
                    if status:
                        return (status, info)
                #Insert into vuln_securityfocus_tag table
                print "Insert into vuln_securityfocus_tag table"
                (status,info) = self.conn_sec.c_search(self.search_tag_id%(item['bugtraq_id']))
                print "236:", info
                if status:
                    return (1,info)
                if tag and info<1:
                    vuln_tag_sent = self.vuln_sec_tag%(item['bugtraq_id'],'9','1',get_localtime_str())
                    (status,info) = self.conn_sec.insert(vuln_tag_sent)
                    if status:
                        return (status,info)
                info = "[upsec]:[{}]:inserted success".format(item['bugtraq_id'])
                return (0,info)
            info = "[upsec]:[{}]:has existed".format(item['bugtraq_id'])
            return (0,info)
        except Exception,e:
            return (1,str(e))

