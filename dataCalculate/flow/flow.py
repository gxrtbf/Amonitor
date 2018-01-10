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

#还款金额情况
def paid():
	timeList = timeScale()
	sql = 'select distinct createDate from dayAddApi_flowpaidmoney'
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

		#还款金额
		print '还款金额数据更新：' + stTime + '~' + edTime
		sql = """
			select sum(repayMoney)
			from loan_repaying 
			where compatibleStatus <> 'CANCEL' and productId != 1001 
			and repaidTime >= '{}' and repaidTime < '{}';
		""".format(stTime,edTime)
		data = pysql.dbInfo(sql)
		data = data.fillna(0)
		money = data.values[0][0]

		sql = """ insert into dayAddApi_flowpaidmoney(paidMoney, createDate) values (%s, %s) """
		dset = [(money,stTime)]
		status = pysql.insertData(sql,dset)
		log.log('每日还款金额更新状态-{}! ({})'.format(status,stTime),'info')
		
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

def c2c():

	timeList = timeScale(startTime='2017-12-10')
	sql = 'select distinct createDate from dayAddApi_flowc2cfund'
	tmRest = pysql.dbInfoLocal(sql)
	tmRest = tmRest.fillna(0)

	tmwait = []
	if not tmRest.empty:
		tmwait = set([str(x)[:10] for x in tmRest['createDate']])

	for i in range(len(timeList)-1):
		stTime = timeList[i]
		edTime = timeList[i+1]

		if stTime in tmwait:
			continue

		print 'c2c数据更新：' + stTime

		c2c_member = config.c2c_member
		for name in c2c_member:

			ids = c2c_member[name][0]
			sql = """
				select count(*) 'num', sum(repayMoney) 'summoney' from loan
				where status = 6 and productId = 7
				and lastUpdated >= '{}' and lastUpdated < '{}'
				and loanerId in ({})
			""".format(stTime,edTime,ids)
			data = pysql.dbInfo(sql)
			data = data.fillna(0)
			loancount = data['num'].values[0]
			loanmoney = data['summoney'].values[0]

			sql = """
				select count(*) 'num', sum(ll.repayMoney) 'summoney' from loan l,loan_repaying ll
				where l.id = ll.loanId 
				and l.status = 6 and l.productId = 7
				and ll.termDate = '{}'
				and l.loanerId in ({})
			""".format(stTime,ids)
			data = pysql.dbInfo(sql)
			data = data.fillna(0)
			loanCountTerm = data['summoney'].values[0]

			sql = """
				select count(*) 'num', sum(lt.repayMoney) 'summoney' from (
				select ll.loanId, ll.repayMoney, ll.repaidTime, ll.termDate from loan l,loan_repaying ll
				where l.id = ll.loanId 
				and l.status = 6 and l.productId = 7
				and ll.termDate = '{}'
				and l.loanerId in ({})) lt
				where DATE_FORMAT(lt.repaidTime,'%Y-%m-%d') > DATE_FORMAT(lt.termDate,'%Y-%m-%d') or lt.repaidTime is null
			""".format(stTime,ids)
			data = pysql.dbInfo(sql)
			data = data.fillna(0)
			loanCountTermNo = data['summoney'].values[0]

			delayRate0 = 0 if loanCountTermNo == 0 else round(loanCountTermNo/float(loanCountTerm)*100,2)

			sql = """
				select count(*) 'num', sum(l.repayMoney) 'summoney' from loan l,loan_repaying ll
				where l.id = ll.loanId
				and l.status = 6 and l.productId = 7 and ll.termDate < '{}'
				and l.loanerId in ({})
			""".format(edTime, ids)
			data = pysql.dbInfo(sql)
			data = data.fillna(0)
			allCountTerm = data['summoney'].values[0]

			sql = """
				select count(*) 'num', sum(ll.repayMoney) 'summoney' from loan l,loan_repaying ll
				where l.id = ll.loanId 
				and l.status = 6 and l.productId = 7
				and l.loanerId in ({})
				and if(ll.repaidTime is null, DATEDIFF(DATE_FORMAT(now(), "%Y-%m-%d"), DATE_FORMAT(ll.termDate, "%Y-%m-%d")), DATEDIFF(DATE_FORMAT(ll.repaidTime, "%Y-%m-%d"), DATE_FORMAT(ll.termDate, "%Y-%m-%d"))) >= 7
			""".format(ids)
			data = pysql.dbInfo(sql)
			data = data.fillna(0)
			countTerm7 = data['summoney'].values[0]

			delayRate7 = 0 if countTerm7==0 else round(countTerm7/float(allCountTerm)*100,2)

			sql = """ insert into dayAddApi_flowc2cfund(member, loanCount, loanMoney, loanCountTerm, loanCountTermNo, delayRate0, allCountTerm, delayRate7, countTerm7, createDate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
			dset = [(name, loancount, loanmoney, loanCountTerm, loanCountTermNo, delayRate0, allCountTerm, delayRate7, countTerm7,stTime)]
			status = pysql.insertData(sql,dset)

			log.log('c2c更新状态-{}！({})！'.format(status,stTime),'info')

def main():
	loan()
	loanNO()
	actRepayment()
	paid()
	c2c()
 
if __name__ == '__main__':
	main()

