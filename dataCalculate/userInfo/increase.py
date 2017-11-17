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

#添加路径
sys.path.insert(0,os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from libfile import pysql
from libfile import logger
import config

#日志
log = logger.Logger('flow-increase',os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "/" + config.log_path)

#路径
def getTheFile(filename):
    return os.path.abspath(os.path.dirname(__file__)) +"/"+filename

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

#数据增长
def userNum():
	timeList = timeScale()
	sql = 'select distinct createDate from dayAddApi_userincrease'
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
		#人数增长
		print '用户增长数据更新：' + stTime + '~' + edTime
		#注册
		sql = """
			select sum(1) from user where date_created > '{}' and date_created < '{}'
		""".format(stTime,edTime)
		data = pysql.dbInfo(sql)
		data = data.fillna(0)
		registerNum = data.values[0][0]

		#申请（新老）
		sql = """
			select count(*) from ci_cash_apply_info 
			where create_time > '{}' and create_time < '{}' 
			and user_id not in (select distinct user_id from ci_cash_apply_info where create_time < '{}');
		""".format(stTime,edTime,stTime)
		data = pysql.dbInfo(sql)
		data = data.fillna(0)
		newApplyNum = data.values[0][0]

		sql = """
			select count(*) from ci_cash_apply_info 
			where create_time > '{}' and create_time < '{}' 
			and user_id in (select distinct user_id from ci_cash_apply_info where create_time < '{}');
		""".format(stTime,edTime,stTime)
		data = pysql.dbInfo(sql)
		data = data.fillna(0)
		oldApplyNum = data.values[0][0]

		#授信
		sql = """
	 		select sum(1) from ci_cash_apply_info where create_time > '{}' and create_time < '{}' and status in ('FA_SUCCESS','SUCCESS')
		""".format(stTime,edTime)
		data = pysql.dbInfo(sql)
		data = data.fillna(0)
		allowNum = data.values[0][0]

		#数据插入
		sql = """ insert into dayAddApi_userincrease(register,allow,newApply,oldApply,createDate) values (%s,%s,%s,%s,%s) """
		dset = [(registerNum,allowNum,newApplyNum,oldApplyNum,stTime)]
		status = pysql.insertData(sql,dset)
		log.log('用户增长数据更新状态{}({})！'.format(status,stTime),'info')

def main():
	userNum()
 
if __name__ == '__main__':
	main()

