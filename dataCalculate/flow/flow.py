# -*- coding: utf-8 -*-
# 
import MySQLdb
import pandas as pd
import numpy
import json
import sys
import os
import datetime

#添加路径
sys.path.insert(0,os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from libfile import pysql
from libfile import logger
import config

#日志
log = logger.Logger('flow',os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "/" + config.log_path)


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

#贷款金额情况
def loan():
	timeList = timeScale()
	sql = 'select distinct createDate from dayAddApi_flowloanmoney'
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

		#借贷金额
		print '借贷金额数据更新：' + stTime + '~' + edTime
		sql = """
			select productId,repayMoney
			from loan_repaying 
			where compatibleStatus <> 'CANCEL' and productId != 1001 
			and createdTime >= '{}' and createdTime < '{}';
		""".format(stTime,edTime)
		data = pysql.dbInfo(sql)
		data = data.fillna(0)
		product = config.product
		for key in product.keys():
			tp = data[data['productId']==int(key)]
			if not tp.empty:
				money = int(sum(tp['repayMoney']))
			else:
				money = 0
			sql = """ insert into dayAddApi_flowloanmoney(product,money,createDate) values (%s,%s,%s) """
			dset = [(product[key],money,stTime)]
			status = pysql.insertData(sql,dset)
		log.log('每日借贷金额更新状态-{}! ({})'.format(status,stTime),'info')
		allLoan = int(sum(data['repayMoney']))
		sql = """ insert into dayAddApi_flowloanmoney(product,money,createDate) values (%s,%s,%s) """
		dset = [('All',allLoan,stTime)]
		status = pysql.insertData(sql,dset)
		log.log('每日借贷金额更新状态-{}! ({})'.format(status,stTime),'info')

	#总金额
	sql = """
		select productId,sum(repayMoney) 'repayMoney'
		from loan_repaying 
		where compatibleStatus <> 'CANCEL' and productId != 1001
		group by productId
	"""
	data = pysql.dbInfo(sql)
	data = data.fillna(0)

	product = config.product
	for key in product.keys():
		proname = product[key]
		tp = data[data['productId']==int(key)]
		if not tp.empty:
		    money = int(sum(tp['repayMoney']))
		else:
		    money = 0
		sql = """ insert into dayAddApi_flowloanmoneysum(product,money,createDate) values (%s,%s,%s) """
		dset = [(proname,money,str(datetime.datetime.today())[:10])]
		status = pysql.insertData(sql,dset)
	log.log('借贷总金额更新状态-{}！({})！'.format(status,stTime),'info')

def loanNO():
	timeList = timeScale()
	sql = 'select distinct createDate from dayAddApi_flowloanmoneyno'
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

		#借贷金额
		print '借贷金额(新老)数据更新：' + stTime + '~' + edTime
		#old
		sql = """
			select sum(repayMoney)
			from loan_repaying 
			where compatibleStatus <> 'CANCEL' and productId != 1001 
			and createdTime >= '{}' and createdTime < '{}'
			and userSid in (select distinct userSid from loan_repaying where createdTime < '{}');
		""".format(stTime,edTime,stTime)
		data = pysql.dbInfo(sql)
		data = data.fillna(0)
		loanOld = data.values[0][0]
		#new
		sql = """
			select sum(repayMoney)
			from loan_repaying 
			where compatibleStatus <> 'CANCEL' and productId != 1001 
			and createdTime >= '{}' and createdTime < '{}'
			and userSid not in (select distinct userSid from loan_repaying where createdTime < '{}');
		""".format(stTime,edTime,stTime)
		data = pysql.dbInfo(sql)
		data = data.fillna(0)
		loanNew = data.values[0][0]

		#插入数据
		sql = """ insert into dayAddApi_flowloanmoneyno(loanOld,loanNew,createDate) values (%s,%s,%s) """
		dset = [(loanOld,loanNew,stTime)]
		status = pysql.insertData(sql,dset)
		log.log('借贷金额(新老)更新状态-{}！({})！'.format(status,stTime),'info')
	

def actRepayment():

	timeList = timeScale()
	sql = 'select distinct createDate from dayAddApi_indexacrepay'
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

		print '应还实还数据更新：' + stTime
		sql = """
			select sum(repayMoney) from loan_repaying
			where termDate='{}' and compatibleStatus not in ('CANCEL')
		""".format(stTime)
		data = pysql.dbInfo(sql)
		data = data.fillna(0)
		allRepayMoney = int(data.values[0][0])

		sql = """
			select sum(repayMoney) from loan_repaying
			where termDate='{}' and compatibleStatus not in ('CANCEL') 
			and repaidTime is not null and DATE_FORMAT(termDate,'%Y-%m-%d') >= DATE_FORMAT(repaidTime,'%Y-%m-%d')
		""".format(stTime)
		data = pysql.dbInfo(sql)
		data = data.fillna(0)
		acRepayMoney = int(data.values[0][0])

		repayRate = int(acRepayMoney/float(allRepayMoney)*100)

		sql = """ insert into dayAddApi_indexacrepay(allRepayMoney,acRepayMoney,repayRate,createDate) values (%s,%s,%s,%s) """
		dset = [(allRepayMoney,acRepayMoney,repayRate,stTime)]
		status = pysql.insertData(sql,dset)

		log.log('每日应还实还更新状态-{}！({})！'.format(status,stTime),'info')

def main():
	loan()
	loanNO()
	actRepayment()
 
if __name__ == '__main__':
	main()

