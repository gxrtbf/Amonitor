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
log = logger.Logger('collect',os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "/" + config.log_path)

#数据包含时间
def timeScale(startTime = "2017-04-15"):
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

def check():
	#催收情况
	sql = """
		select month, round(D4催回金额/D4逾期金额*100,2) 'day4Rate',
		round(D7催回金额/D7逾期金额*100,2) 'day7Rate',
		round(D15催回金额/D15逾期金额*100,2) 'day15Rate',
		round(D30催回金额/D30逾期金额*100,2) 'day30Rate',
		round(D60催回金额/D60逾期金额*100,2) 'day60Rate',
		round(D90催回金额/D90逾期金额*100,2) 'day90Rate',
		round(D90Plus催回金额/D90逾期金额*100,2) 'day90Ratem'
		from (
		select date_format(a.lendTime,'%Y-%m') 'month', 
		sum(case when datediff(now(), b.termDate) >= 4 and b.compatibleStatus in ('OVERDUE','OVERDUE_PAID')
		then a.payMoney else 0 end) 'D4逾期金额',
		sum(case when datediff(now(), b.termDate) >= 7 and b.compatibleStatus in ('OVERDUE','OVERDUE_PAID')
		then a.payMoney else 0 end) 'D7逾期金额',
		sum(case when datediff(now(), b.termDate) >= 15 and b.compatibleStatus in ('OVERDUE','OVERDUE_PAID')
		then a.payMoney else 0 end) 'D15逾期金额',
		sum(case when datediff(now(), b.termDate) >= 30 and b.compatibleStatus in ('OVERDUE','OVERDUE_PAID')
		then a.payMoney else 0 end) 'D30逾期金额',
		sum(case when datediff(now(), b.termDate) >= 60 and b.compatibleStatus in ('OVERDUE','OVERDUE_PAID')
		then a.payMoney else 0 end) 'D60逾期金额',
		sum(case when datediff(now(), b.termDate) >= 90 and b.compatibleStatus in ('OVERDUE','OVERDUE_PAID')
		then a.payMoney else 0 end) 'D90逾期金额',
		sum(case when datediff(now(), b.termDate) >= 4 and b.compatibleStatus = 'OVERDUE_PAID' and b.repaidTime <= adddate(b.termDate, interval+4 day) 
		then a.payMoney else 0 end) 'D4催回金额',
		sum(case when datediff(now(), b.termDate) >= 7 and b.compatibleStatus = 'OVERDUE_PAID' and b.repaidTime <= adddate(b.termDate, interval+7 day) 
		then a.payMoney else 0 end) 'D7催回金额',
		sum(case when datediff(now(), b.termDate) >= 15 and b.compatibleStatus = 'OVERDUE_PAID' and b.repaidTime <= adddate(b.termDate, interval+15 day) 
		then a.payMoney else 0 end) 'D15催回金额',
		sum(case when datediff(now(), b.termDate) >= 30 and b.compatibleStatus = 'OVERDUE_PAID' and b.repaidTime <= adddate(b.termDate, interval+30 day) 
		then a.payMoney else 0 end) 'D30催回金额',
		sum(case when datediff(now(), b.termDate) >= 60 and b.compatibleStatus = 'OVERDUE_PAID' and b.repaidTime <= adddate(b.termDate, interval+60 day) 
		then a.payMoney else 0 end) 'D60催回金额',
		sum(case when datediff(now(), b.termDate) >= 90 and b.compatibleStatus = 'OVERDUE_PAID' and b.repaidTime <= adddate(b.termDate, interval+90 day) 
		then a.payMoney else 0 end) 'D90催回金额',
		sum(case when datediff(now(), b.termDate) >= 90 and b.compatibleStatus = 'OVERDUE_PAID'
		then a.payMoney else 0 end) 'D90Plus催回金额'
		from loan a, loan_repaying b
		where a.id = b.loanId and a.status = 6 and b.termDate < curdate() and a.productId not in (3,4)
		#and not exists (select 1 from loan g where g.userSid = a.userSid and g.status = 6 and g.lendTime < a.lendTime)
		group by month) a;
	"""
	data = pysql.dbInfo(sql)
	data = data.fillna(0)

	month = list(data['month'])
	day4Rate = list(data['day4Rate'])
	day7Rate = list(data['day7Rate'])
	day15Rate = list(data['day15Rate'])
	day30Rate = list(data['day30Rate'])
	day60Rate = list(data['day60Rate'])
	day90Rate = list(data['day90Rate'])
	day90Ratem = list(data['day90Ratem'])
	updateDate = [str(datetime.datetime.today())[:10]] * len(month)

	sql = "delete from dayAddApi_CollectRate"
	status = pysql.deletetData(sql)
	log.log(u'催回率数据删除状态-{}!({})'.format(status,str(datetime.date.today())),'info')

	sql = """ insert into dayAddApi_CollectRate(month,day4Rate,day7Rate,day15Rate,day30Rate,day60Rate,day90Rate,day90Ratem,createDate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
	dset = zip(month,day4Rate,day7Rate,day15Rate,day30Rate,day60Rate,day90Rate,day90Ratem,updateDate)
	status = pysql.insertData(sql,dset)
	log.log('催回率数据更新状态-{}！({})！'.format(status,str(datetime.date.today())),'info')


def collectDisYesterday():
	#案件数量情

	#每日数据 当前逾期天数的分布
	timeList = timeScale()
	sql = 'select distinct createDate from dayAddApi_CollectDis'
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

		print '案件数量' + stTime
		curDisct = {}

		#待催收的案件数(未完成的催回+在规定时间外催回的)
		sql = """
			select count(*) from t_loan_case
			where firm_id = 1 and create_date < '{}' and repaid_date > '{}' and loan_status = 'PAID'
		""".format(edTime,edTime)
		data = pysql.dbInfoCollect(sql)
		data = data.fillna(0)
		sql = """
			select count(*) from t_loan_case
			where loan_status = 'OVERDUE' and firm_id = 1 and create_date < '{}'
		""".format(edTime)
		data1 = pysql.dbInfoCollect(sql)
		data1 = data1.fillna(0)
		currentNum = data.values[0][0] + data1.values[0][0]
		curDisct['currentNum'] = currentNum

		#待催收的案件逾期天数分布
		sql = """
			select DATEDIFF('{}',overdue_date) 'overdue_day' from t_loan_case
			where firm_id = 1 and create_date < '{}' and repaid_date > '{}' and loan_status = 'PAID'
		""".format(edTime,edTime,edTime)
		data = pysql.dbInfoCollect(sql)

		sql = """
			select DATEDIFF('{}',overdue_date) 'overdue_day' from t_loan_case
			where loan_status = 'OVERDUE' and firm_id = 1 and create_date < '{}'
		""".format(edTime,edTime)
		data1 = pysql.dbInfoCollect(sql)

		overdue_day_list = []
		for x in data['overdue_day']:
			overdue_day_list.append(x)
		for x in data1['overdue_day']:
			overdue_day_list.append(x)

		bins = [0,3,10,20,30,60,90,max(overdue_day_list)+1]
		labels = ['1-3','4-10','11-20','21-30','31-60','61-90','90-']
		df = pd.cut(overdue_day_list,bins=bins,labels=labels)
		df = df.value_counts()
		for i in range(len(df)):
			curDisct[df.index[i]] = df.values[i]

		sql = """ insert into dayAddApi_CollectDis(dayto3,dayto10,dayto20,dayto30,dayto60,dayto90,dayover90,currentNum,createDate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
		dset = [(curDisct['1-3'],curDisct['4-10'],curDisct['11-20'],curDisct['21-30'],curDisct['31-60'],curDisct['61-90'],curDisct['90-'],curDisct['currentNum'],stTime)]
		status = pysql.insertData(sql,dset)
		log.log('每日案件逾期天数更新状态-{}! ({})'.format(status,stTime),'info')

def collectNumYesterday():
	#每日数据 
	timeList = timeScale()
	sql = 'select distinct createDate from dayAddApi_CollectNum'
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

		print '催收每日数据' + stTime
		#新增案件数
		sql = """
			select count(*) from t_loan_case
			where create_date like '{}%' and firm_id = 1
		""".format(stTime)
		data = pysql.dbInfoCollect(sql)
		data = data.fillna(0)
		yesterdayNew = data.values[0][0]

		#催回案件数（30天以上委外 30天以下自催）
		sql = """
			select count(*) from t_loan_case
			where repaid_date like '{}%' and firm_id = 1 and overdue_day >= 30
		""".format(stTime)
		data = pysql.dbInfoCollect(sql)
		data = data.fillna(0)
		yesterdayPaidl30 = data.values[0][0]

		sql = """
			select count(*) from t_loan_case
			where repaid_date like '{}%' and firm_id = 1 and overdue_day < 30
		""".format(stTime)
		data = pysql.dbInfoCollect(sql)
		data = data.fillna(0)
		yesterdayPaidu30 = data.values[0][0]

		#催回 三日前的应催案件数
		threeDay = str(datetime.datetime.strptime(stTime, '%Y-%m-%d') - datetime.timedelta(days=3))[:10]
		sql = """
			select count(*) from t_loan_case
			where create_date like '{}%' and firm_id = 1
		""".format(threeDay)
		data = pysql.dbInfoCollect(sql)
		data = data.fillna(0)
		threeDayPaing = data.values[0][0]

		#催回 三日前的催回案件数
		sql = """
			select count(*) from t_loan_case
			where create_date like '{}%' and repaid_date <= '{}' and firm_id = 1
		""".format(threeDay,edTime)
		data = pysql.dbInfoCollect(sql)
		data = data.fillna(0)
		threeDayPaid = data.values[0][0]

		#昨日 三日催回率
		if threeDayPaing != 0:
			NewPaidRate = round(threeDayPaid/float(threeDayPaing)*100,2)
		else:
			NewPaidRate = 0

		sql = """ insert into dayAddApi_CollectNum(newAdd,newCollectMl1,newCollectMu1,threeDayCollect,threeDayCollectRate,createDate) values (%s,%s,%s,%s,%s,%s) """
		dset = [(yesterdayNew,yesterdayPaidl30,yesterdayPaidu30,threeDayPaing,NewPaidRate,stTime)]
		status = pysql.insertData(sql,dset)
		log.log('催回基本数据更新状态-{}! ({})'.format(status,stTime),'info')

def main():
	check()
	collectDisYesterday()
	collectNumYesterday()

if __name__ == '__main__':
	main()

