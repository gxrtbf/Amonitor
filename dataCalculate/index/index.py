# -*- coding: utf-8 -*-
# 
import MySQLdb
import pandas as pd
import numpy
import json
import sys
import os
import datetime
import time

reload(sys)  
sys.setdefaultencoding('utf8') 

#添加路径
sys.path.insert(0,os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from libfile import pysql
from libfile import logger
import config

#日志
log = logger.Logger('index',os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "/" + config.log_path)

#路径
def getTheFile(filename):
    return os.path.abspath(os.path.dirname(__file__)) +"/"+filename

#用户漏斗
def hopperHead():

	sql = """select count(*) from user;"""
	data = pysql.dbInfo(sql)
	registerNum = data.values[0][0]

	sql = """select count(distinct user_id) from ci_cash_apply_info;"""
	data = pysql.dbInfo(sql)
	applyNum = data.values[0][0]

	sql = """select count(DISTINCT user_id) from ci_cash_apply_info where status in ('FA_SUCCESS','SUCCESS');"""
	data = pysql.dbInfo(sql)
	passNum = data.values[0][0]

	sql = """select count(*) from batch_acc_mgnt_account_info;"""
	data = pysql.dbInfo(sql)
	loanNum = data.values[0][0]

	sql = """select count(*) from batch_acc_mgnt_account_info where loan_times >=2;"""
	data = pysql.dbInfo(sql)
	reloanNum = data.values[0][0]

	#数据插入
	sql = """ insert into dayAddApi_indexhopper(register,applys,passs,loan,reloan,createDate) values (%s,%s,%s,%s,%s,%s) """
	dset = [(registerNum,applyNum,passNum,loanNum,reloanNum,str(datetime.datetime.now()-datetime.timedelta(days=1))[:10])]
	status = pysql.insertData(sql,dset)
	log.log('漏斗数据更新状态-{}'.format(status),'info')


	#基本总量情况
	sumUser = registerNum
	activeUser = loanNum

	sql = """select count(*) from loan where status=6;"""
	data = pysql.dbInfo(sql)
	tradeNum = data.values[0][0]

	sql = """select sum(lendMoney) from loan where status=6;"""
	data = pysql.dbInfo(sql)
	tradeMoney = int(data.values[0][0])

	#数据插入
	sql = """ insert into dayAddApi_indexhead(sumUser,activeUser,tradeNum,tradeMoney,createDate) values (%s,%s,%s,%s,%s) """
	dset = [(sumUser,activeUser,tradeNum,tradeMoney,str(datetime.datetime.now()-datetime.timedelta(days=1))[:10])]
	status = pysql.insertData(sql,dset)
	log.log('首页标题数据更新状态-{}！'.format(status),'info')

#用户地区分布
def userPlace():
	
	sql = """
		select aes_decrypt(a.id_num,'1zhida**') 'id_num' from _user a,batch_acc_mgnt_account_info b where a.id=b.user_id;
	"""
	data = pysql.dbInfo(sql)
	id_init = pd.read_csv(getTheFile('../data/t_id_card_init.csv'))
	id_init['code'] = id_init['code'].map(str)
	province = id_init[id_init['code'].map(lambda x:str(x)[-4:]=='0000')]
	province1 = province[province['name'].map(lambda x: '北京'in x or '上海' in x or '天津'in x or '重庆' in x)]   
	province2 = province[province['name'].map(lambda x: '市' not in x)] 
	province = pd.concat([province1,province2])
	city = id_init[id_init['code'].map(lambda x:str(x)[-2:]=='00')]
	data['province_t'] = data['id_num'].map(lambda x:str(x)[:2]+'0000')
	data['city_t'] = data['id_num'].map(lambda x:str(x)[:4]+'00')
	data['country_t'] = data['id_num'].map(lambda x:str(x)[:6])
	data = pd.merge(data,province,left_on='province_t',right_on='code',how='left')
	data['省'] = data['name']
	del data['code']
	del data['name']
	data = pd.merge(data,city,left_on='city_t',right_on='code',how='left')
	data['市'] = data['name']
	del data['code']
	del data['name']
	del data['province_t']
	del data['city_t']
	del data['country_t']
	data["人数"] = 1
	tp = pd.pivot_table(data,index=['省','市'],values=["人数"],aggfunc='count',fill_value=0)
	tp['省'] = tp.index.map(lambda x :x[0])
	tp['市'] = tp.index.map(lambda x :x[1])
	tp = tp.sort_values(by="人数",ascending=False)
	tp = tp.reset_index(drop=True)

	#生成city
	# gg = {}
	# for i in range(len(tp)):
	# 	item = tp.ix[i]
	# 	key = item['省'] + item['市']
	# 	gg[key] = item['市'].replace("地区","").replace("市","")
	# 	if i > 71:
	# 		break
	# json.dump(gg, open(getTheFile('data/city.json'), 'w'), default=config.set_default)

	city = json.load(open(getTheFile('../data/city.json')))
	cityName = []
	cityNum = []
	for i in range(50,-1,-1):
		item = tp.ix[i]
		key = item['省'].decode('utf-8') + item['市'].decode('utf-8')
		cityName.append(city[key])
		cityNum.append(item['人数'])
	ctime = [str(datetime.datetime.now()-datetime.timedelta(days=1))[:10]]*len(cityName)

	sql = """ insert into dayAddApi_indexcity(cityName,numInCity,createDate) values (%s,%s,%s) """
	cityName = [x.decode("utf-8") for x in cityName]
	dset = zip(cityName,cityNum,ctime)
	status = pysql.insertData(sql,dset)

	log.log('用户地区分布数据更新状态-{}！'.format(status),'info')

	# city = json.load(open(getTheFile('../static/data/index/city_value.json')))
	# data_dict = {}
	# import requests
	# import string
	# for key in city.keys():
	# 	values = {'place' : key}
	# 	url = string.Template('http://maps.googleapis.com/maps/api/geocode/json?address=$place&sensor=false&language=zh-CN')
	# 	url = url.safe_substitute(values)
	# 	r = requests.get(url=url,headers=None,timeout=10)
	# 	rj = json.loads(r.text)
	# 	if rj.get('status') == 'OK':
	# 		rj = rj['results'][0]
	# 		data_dict[key] = [rj['geometry']['location']['lng'],rj['geometry']['location']['lat']]
	# json.dump(data_dict, open(getTheFile('../static/data/index/city_zuobiao.json'), 'w'), default=config.set_default)

	# city = json.load(open(getTheFile('../static/data/index/city_value.json')))
	# data_dict = []
	# for key in city.keys():
	# 	temp = {}
	# 	temp['name'] = key
	# 	temp['value'] = 'dateset["'+ key+'""]'
	# 	data_dict.append(temp)
	# json.dump(data_dict, open(getTheFile('../static/data/index/city_test.json'), 'w'), default=config.set_default)

#仪表盘数据 平均借贷金额  平均借贷天数 平均服务费用
def dashbook():
	
	dashBook = {}
	sql = """select avg(a.repayMoney) 'avgMoney' from loan_repaying a left join loan b
			on a.loanId = b.id
			where DateDiff(a.createdTime,now())=-1"""
	data = pysql.dbInfo(sql)
	avgMoney = round(data.values[0][0],2)

	sql = """
		select avg(b.termNum) 'avgTermNum' from loan_repaying a left join loan b
		on a.loanId = b.id
		where DateDiff(a.createdTime,now())=-1
	"""
	data = pysql.dbInfo(sql)
	avgTermNum = round(data.values[0][0],2)

	sql = """
		select avg(b.repayMoney - b.payMoney) 'avgServiceMoney' from loan_repaying a left join loan b
		on a.loanId = b.id
		where DateDiff(a.createdTime,now())=-1
	"""
	data = pysql.dbInfo(sql)
	avgServiceMoney = round(data.values[0][0],2)

	sql = """ insert into dayAddApi_indexdash(avgTermNum,avgMoney,avgServiceMoney,createDate) values (%s,%s,%s,%s) """
	dset = [(avgTermNum,avgMoney,avgServiceMoney,str(datetime.datetime.now()-datetime.timedelta(days=1))[:10])]
	status = pysql.insertData(sql,dset)

	log.log('仪表盘数据更新状态-{}！'.format(status),'info')

def main():
	hopperHead()
	userPlace()
	dashbook()
 
if __name__ == '__main__':
	main()

