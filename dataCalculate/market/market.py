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
import gc

#添加路径
sys.path.insert(0,os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from libfile import pysql
from libfile import logger
import config

#日志
log = logger.Logger('market',os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "/" + config.log_path)

#路径
def getTheFile(filename):
    return os.path.abspath(os.path.dirname(__file__)) +"/"+filename

#数据包含时间
def timeScale(startTime = "2017-05-01"):
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

def passRateloan():

	endTime = str(datetime.date.today()-datetime.timedelta(days=3))

	timeList = timeScale('2017-05-01')
	sql = 'select distinct createDate from marketNum'
	tmRest = pysql.dbInfoLocal(sql)
	tmRest = tmRest.fillna(0)

	tmwait = []
	if not tmRest.empty:
		tmwait = [str(x)[:10] for x in tmRest['createDate']]

	for i in range(len(timeList)-1):
		stTime = timeList[i]
		edTime1 = timeList[i+1]

		if stTime in tmwait and stTime < endTime:

			#当前提现成功率
			sql = """
				select count(DISTINCT b.userSid) from ci_cash_apply_info a,loan b
				where a.user_id=b.userSid and a.product_id = b.productId 
				and a.audit_date >= '{}' and a.audit_date < '{}' 
				and b.createdTime > '{}'
				and a.status in ('SUCCESS','FA_SUCCESS') and b.status=6;
			""".format(stTime,edTime1,stTime)
			data = pysql.dbInfo(sql)
			data = data.fillna(0)
			paidNum = data.values[0][0]

			#当前提现成功率
			sql = """
				select datPass from marketNum
				where createDate >= '{}' and createDate < '{}' 
			""".format(stTime,edTime)
			data = pysql.dbInfo(sql)
			data = data.fillna(0)
			applyPass = data.values[0][0]
			#当前 申请提现成功率
			paidRate = round(paidNum/float(applyPass*100,2)) if paidNum > 2 else 0
			#存储数据
			sql = """ 
				update marketNum 
	   			set nowSucMoneyRate = {} 
	 			where createDate >= '{}' and createDate < '{}' 
			""".format(paidRate,stTime,edTime1)
			status = pysql.updateData(sql)
			log.log('当前申请提现成功率更新状态-{}! ({})'.format(status,stTime),'info')
			continue

		print '提现情况' + stTime

		#每日数据模板
		dayNum = {
			'applyPass':0,
			'firstDayT':0,
			'firstDay':0,
			'firstDayRate':0,
			'tryRate':0,
			'secondDay':0,
			'secondDayRate':0,
			'thirdDay':0,
			'thirdDayRate':0,
			'paidNum':0,
			'paidRate':0,
			'auditTime':0,
			'auditTimeWit':0,
			'auditTimeToday':0
		}

		#每日审核通过情况
		sql = """
			select count(distinct user_id) from ci_cash_apply_info 
			where audit_date > '{}' and audit_date < '{}' and status in ('SUCCESS','FA_SUCCESS')
		""".format(stTime,edTime1)
		data = pysql.dbInfo(sql)
		data = data.fillna(0)
		dayNum['applyPass'] = data.values[0][0]

		#当日审核 申请提现
		sql = """
			select count(DISTINCT b.userSid) from ci_cash_apply_info a,loan b
			where a.user_id=b.userSid and a.product_id = b.productId 
			and a.audit_date > '{}' and a.audit_date < '{}' 
			and b.createdTime > '{}' and b.createdTime < '{}' 
			and a.status in ('SUCCESS','FA_SUCCESS');
		""".format(stTime,edTime1,stTime,edTime1)
		data = pysql.dbInfo(sql)
		data = data.fillna(0)
		dayNum['firstDayT'] = data.values[0][0]

		#当日审核 申请提现成功
		sql = """
			select count(DISTINCT b.userSid) from ci_cash_apply_info a,loan b
			where a.user_id=b.userSid and a.product_id = b.productId 
			and a.audit_date > '{}' and a.audit_date < '{}' 
			and b.createdTime > '{}' and b.createdTime < '{}' 
			and a.status in ('SUCCESS','FA_SUCCESS') and b.status=6;
		""".format(stTime,edTime1,stTime,edTime1)
		data = pysql.dbInfo(sql)
		data = data.fillna(0)
		dayNum['firstDay'] = data.values[0][0]

		#当日审核 申请提现率
		dayNum['tryRate'] = round(dayNum['firstDayT']/float(dayNum['applyPass'])*100,2) if dayNum['applyPass'] > 2 else 0
		#当日审核 申请提现成功率
		dayNum['firstDayRate'] = round(dayNum['firstDay']/float(dayNum['applyPass'])*100,2) if dayNum['applyPass'] > 2 else 0

		#当前提现成功
		sql = """
			select count(DISTINCT b.userSid) from ci_cash_apply_info a,loan b
			where a.user_id=b.userSid and a.product_id = b.productId 
			and a.audit_date > '{}' and a.audit_date < '{}' 
			and b.createdTime > '{}'
			and a.status in ('SUCCESS','FA_SUCCESS') and b.status=6;
		""".format(stTime,edTime1,stTime)
		data = pysql.dbInfo(sql)
		data = data.fillna(0)
		dayNum['paidNum'] = data.values[0][0]
		
		#当前 申请提现成功率
		dayNum['paidRate'] = round(dayNum['paidNum']/float(dayNum['applyPass'])*100,2) if dayNum['applyPass'] > 2 else 0

		#审核时间
		sql = """
			select DATE_FORMAT(create_time,'%H') 'hour',(UNIX_TIMESTAMP(audit_date) - UNIX_TIMESTAMP(create_time)) 'wait_second' 
			from ci_cash_apply_info
			where audit_date is not null and status in ('SUCCESS','FA_SUCCESS') 
			and audit_date > '{}' and audit_date < '{}'
		""".format(stTime,edTime1)
		data = pysql.dbInfo(sql)
		data = data.fillna(0)
		if len(data) > 10:
			lp = data['wait_second']
			lp = lp[lp>np.percentile(data['wait_second'],15)]
			lp = lp[lp<np.percentile(data['wait_second'],85)]
			dayNum['auditTime'] = int(np.mean(lp)/60)

		data = data[data['hour'].map(lambda x: x not in ['22','23','00','01','02','03','04','05','06'])]
		if not data.empty:
			if len(data) > 10:
				lp = data['wait_second']
				lp = lp[lp>np.percentile(data['wait_second'],15)]
				lp = lp[lp<np.percentile(data['wait_second'],85)]
				dayNum['auditTimeWit'] = int(np.mean(lp)/60)

		#当日的审核情况
		sql = """
			select DATE_FORMAT(create_time,'%H') 'hour',(UNIX_TIMESTAMP(audit_date) - UNIX_TIMESTAMP(create_time)) 'wait_second' 
			from ci_cash_apply_info
			where audit_date is not null and status in ('SUCCESS','FA_SUCCESS') and DATE_FORMAT(audit_date,'%Y-%m-%d')=DATE_FORMAT(create_time,'%Y-%m-%d')
			and audit_date > '{}' and audit_date < '{}'
		""".format(stTime,edTime1)
		data = pysql.dbInfo(sql)
		data = data.fillna(0)
		data = data[data['hour'].map(lambda x: x not in ['22','23','00','01','02','03','04','05','06'])]
		if len(data) > 10:
			lp = data['wait_second']
			lp = lp[lp>np.percentile(data['wait_second'],15)]
			lp = lp[lp<np.percentile(data['wait_second'],85)]
			dayNum['auditTimeToday'] = int(np.mean(lp)/60)

		sql = """ insert into marketNum(applyPass,firstDayT,firstDay,firstDayRate,tryRate,secondDay,secondDayRate,thirdDay,thirdDayRate,paidNum,paidRate,auditTime,auditTimeWit,auditTimeToday,createDate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
		dset = [(
			dayNum['applyPass'] ,
			dayNum['firstDayT'] ,
			dayNum['firstDay'] ,
			dayNum['firstDayRate'] ,
			dayNum['tryRate'] ,
			dayNum['secondDay'] ,
			dayNum['secondDayRate'] ,
			dayNum['thirdDay'] ,
			dayNum['thirdDayRate'] ,
			dayNum['paidNum'] ,
			dayNum['paidRate'] ,
			dayNum['auditTime'] ,
			dayNum['auditTimeWit'] ,
			dayNum['auditTimeToday'] ,
			stTime
			)]
		status = pysql.insertData(sql,dset)
		log.log(u'逾审核时间数据更新更新状态-{}！({})！'.format(status,stTime),'info')

def main():
	passRateloan()
	

def strtotime(strtime):
    if type(strtime) in [pd.tslib.NaTType]:
        strtime = datetime.datetime.now()
    return strtime
 
if __name__ == '__main__':
	main()

