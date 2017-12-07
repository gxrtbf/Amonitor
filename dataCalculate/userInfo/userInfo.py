# -*- coding: utf-8 -*-
# 
import MySQLdb
import pandas as pd
import numpy as np
import sys
import os
import datetime
import dateutil

#添加路径
sys.path.insert(0,os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from libfile import pysql
from libfile import logger
import config


#日志
log = logger.Logger('userInfo',os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "/" + config.log_path)


#数据包含时间
def timeScale(startTime = "2017-03-01"):
	nowTime = datetime.date.today()
	i = 0
	timeList = []
	while True:
		endTime = str(nowTime-datetime.timedelta(days=i))
		timeList.insert(0,endTime)
		if endTime == startTime:
			break
		i = i + 1
	return timeList

#数据包含时间 month
def timeScaleMonth(startTime = "2017-03-01"):
	nowTime = datetime.date.today()
	i = 0
	timeList = []
	while True:
		endTime = str(nowTime-dateutil.relativedelta.relativedelta(months=i))
		if endTime < startTime:
			break
		timeList.insert(0,endTime[:7])
		i = i + 1
	return timeList

def userSex():
	#分性别的注册用户
	#男
	sql = """
		select count(sex) 'num' from user where sex = '1';
	"""
	data = pysql.dbInfo(sql)
	data = data.fillna(0)
	male = data.values[0][0]

	#女
	sql = """
		select count(sex) 'num' from user where sex = '2';
	"""
	data = pysql.dbInfo(sql)
	data = data.fillna(0)
	female = data.values[0][0]

	sql = """ insert into dayAddApi_usersexall(male,female,createDate) values (%s,%s,%s) """
	dset = [(male,female,str(datetime.datetime.now())[:10])]
	status = pysql.insertData(sql,dset)

	log.log('用户性别（总）更新状态-{}！'.format(status),'info')

 	#日增数据
	timeList = timeScale()
	sql = 'select distinct createDate from dayAddApi_usersex'
	tmRest = pysql.dbInfoLocal(sql)
	tmRest = tmRest.fillna(0)

	tmwait = []
	if not tmRest.empty:
		tmwait = [str(x)[:10] for x in tmRest['createDate']]

	for i in range(len(timeList)-1):
		stTime = timeList[i]
		edTime = timeList[i+1]

		if stTime in tmwait:
			continue

		print '性别' + stTime
		sql = """
			select count(*) from user where date_created > '{}' and date_created < '{}' and sex = '1'
		""" .format(stTime,edTime)
		data = pysql.dbInfo(sql)
		data = data.fillna(0)
		male = data.values[0][0]

		sql = """
			select count(*) from user where date_created > '{}' and date_created < '{}' and sex = '2'
		""" .format(stTime,edTime)
		data = pysql.dbInfo(sql)
		data = data.fillna(0)
		female = data.values[0][0]

		sql = """ insert into dayAddApi_usersex(male,female,createDate) values (%s,%s,%s) """
		dset = [(male,female,stTime)]
		status = pysql.insertData(sql,dset)
		log.log('用户性别（日）更新状态-{}！({})'.format(status,stTime),'info')


def userAge():
	#分年龄的注册用户
	sql = """
		select age,count(age) 'num' from user where age <> 0 group by age;
	"""
	data = pysql.dbInfo(sql)
	age_label = config.age_label
	data['age'] = pd.cut(data['age'],age_label['point'],labels=age_label['label'])
	data = pd.pivot_table(data,index=["age"],values=["num"],aggfunc='sum')
	data['age'] = data.index

	sql = """ insert into dayAddApi_userageall(age1,age2,age3,age4,age5,createDate) values (%s,%s,%s,%s,%s,%s) """
	dset = [(data['num'][0],data['num'][1],data['num'][2],data['num'][3],data['num'][4],str(datetime.datetime.now())[:10])]
	status = pysql.insertData(sql,dset)
	log.log('用户年龄（总）更新状态-{}！'.format(status),'info')


	timeList = timeScale()
	sql = 'select distinct createDate from dayAddApi_userage'
	tmRest = pysql.dbInfoLocal(sql)
	tmRest = tmRest.fillna(0)

	tmwait = []
	if not tmRest.empty:
		tmwait = [str(x)[:10] for x in tmRest['createDate']]

	for i in range(len(timeList)-1):
		stTime = timeList[i]
		edTime = timeList[i+1]

		if stTime in tmwait:
			continue
		print '年龄' + stTime
		sql = """
			select age,count(age) 'num' from user where age <> 0 and date_created > '{}' and date_created < '{}' group by age;
		""".format(stTime,edTime)
		data = pysql.dbInfo(sql)
		age_label = config.age_label
		data['age'] = pd.cut(data['age'],age_label['point'],labels=age_label['label'])
		data = pd.pivot_table(data,index=["age"],values=["num"],aggfunc='sum')
		data['age'] = data.index

		sql = """ insert into dayAddApi_userage(age1,age2,age3,age4,age5,createDate) values (%s,%s,%s,%s,%s,%s) """
		dset = [(data['num'][0],data['num'][1],data['num'][2],data['num'][3],data['num'][4],stTime)]
		status = pysql.insertData(sql,dset)
		log.log('用户年龄（日）更新状态-{}！({})'.format(status,stTime),'info')

def userRest():

	timeList = timeScaleMonth()
	sql = 'select distinct createDate from dayAddApi_userrest'
	tmRest = pysql.dbInfoLocal(sql)
	tmRest = tmRest.fillna(0)

	tmwait = []
	if not tmRest.empty:
		tmwait = [str(x)[:7] for x in tmRest['createDate']]

	for i in range(len(timeList)-1):
		stTime = timeList[i]
		edTime = timeList[i+1]

		if stTime in tmwait:
			continue

		print u'留存' + stTime
		sql = """
			select DATE_FORMAT(a.audit_date,'%Y-%m') 'month',count(distinct a.user_id) 'allrest' from (
			select c.user_id,c.audit_date from ci_cash_apply_info c left join user u
			on c.user_id=u.id
			where c.status='SUCCESS' and u.date_created > '{}' and u.date_created < '{}'
			) a
			where a.audit_date = (
			select min(b.audit_date) from ci_cash_apply_info b where a.user_id=b.user_id and b.status='SUCCESS' and b.create_time > '{}'
			)
			group by DATE_FORMAT(a.audit_date,'%Y-%m')
		""".format(stTime + '-01',edTime + '-01',stTime + '-01')
		allrest = pysql.dbInfo(sql)
		allrest = allrest.fillna(0)

		sql = """
			select DATE_FORMAT(a.createdTime,'%Y-%m') 'month',count(distinct a.userSid) 'currentactive' from (
			select l.userSid,l.createdTime from loan l left join user u
			on l.userSid=u.id
			where l.status=6 and u.date_created > '{}' and u.date_created < '{}' ) a 
			group by DATE_FORMAT(a.createdTime,'%Y-%m')
		""".format(stTime + '-01',edTime + '-01')
		cactive = pysql.dbInfo(sql)
		cactive = cactive.fillna(0)

		aad = pd.merge(allrest,cactive,how='outer')
		aad = aad.fillna(0)
		aad['allrest'] = [sum(aad['allrest'][:(i+1)]) for i in range(len(aad))]
		aad['rtime'] = stTime
		aad['activerate'] = aad['currentactive']/aad['allrest']*100
		aad['createdTime'] = str(datetime.datetime.now())[:10]

		rtime = list(aad['rtime'])
		cmonth = list(aad['month'])
		allrest = list(aad['allrest'])
		currentactive = list(aad['currentactive'])
		currentActiveRate = list(aad['activerate'])
		ctime = list(aad['createdTime'])

		sql = "delete from dayAddApi_userrest where registerDate='{}'".format(stTime)
		status = pysql.deletetData(sql)
		log.log(u'留存数据删除状态-{}！'.format(status),'info')

		sql = """ insert into dayAddApi_userrest(registerDate,currentDate,allPass,currentActive,currentActiveRate,createDate) values (%s,%s,%s,%s,%s,%s) """
		dset = zip(rtime,cmonth,allrest,currentactive,currentActiveRate,ctime)
		status = pysql.insertData(sql,dset)
		log.log('留存数据更新状态-{}！({})'.format(status,stTime),'info')


def main():
	userSex()
	userAge()
	userRest()

if __name__ == '__main__':
	main()

