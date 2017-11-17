# -*- coding: utf-8 -*-
# 
import MySQLdb
import pandas as pd
import numpy as np
import json
import sys
import os
import logging
import datetime

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

def main():
	userSex()
	userAge()

if __name__ == '__main__':
	main()

