# -*- coding: utf-8 -*-
# 
import MySQLdb
import pandas as pd
import numpy
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
log = logger.Logger('flow',os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "/" + config.log_path)

#路径
def getTheFile(filename):
    return os.path.abspath(os.path.dirname(__file__)) +"/"+filename

#数据包含时间
def timeScale(startTime = "2017-09-01"):
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

#逾期情况 根据资金方区分
def delayDayFund():

	fundId = config.fundloanId
	for fundName in fundId.keys():
		ids = fundId[fundName][0]
		#逾期情况 not in (3,4,5,6,1001)
		sql = """
			select DATE_FORMAT(b.termDate,'%Y-%m-%d') 'date',sum(a.payMoney) 'allPayMoney',sum(b.repayMoney+b.overdueInterest+b.overdueFee) 'allMoney' from loan a,loan_repaying b 
			where a.id=b.loanId and a.status=6 and b.compatibleStatus not in ('UNPAID','CANCEL') and a.fundPayAccountId in ({})
			and b.productId not in (3,4,5,6,1001)
			and b.termDate < DATE_FORMAT(now(),'%Y-%m-%d')
			GROUP BY DATE_FORMAT(b.termDate,'%Y-%m-%d');
		""".format(ids)
		alldata = pysql.dbInfo(sql)
		alldata = alldata.fillna(0)
		delayPoint = [0,3,7,10,20,30,60,90]
		pp = []
		for day in delayPoint:
			sql = """
				select DATE_FORMAT(c.termDate,'%Y-%m-%d') 'date',sum(c.payMoney) 'payMoney' from (
				select a.payMoney,b.* from loan a,loan_repaying b 
				where a.id=b.loanId and a.status=6 and b.compatibleStatus not in ('UNPAID','CANCEL') and b.productId not in (3,4,5,6,1001)
				and a.fundPayAccountId in ({})
				and b.termDate < DATE_FORMAT(now(),'%Y-%m-%d')
				HAVING if(b.repaidTime is NULL,TO_DAYS(now()) - TO_DAYS(b.termDate),TO_DAYS(b.repaidTime) - TO_DAYS(b.termDate)) <= {}) c
				GROUP BY DATE_FORMAT(c.termDate,'%Y-%m-%d');
			""".format(ids,day)
			data = pysql.dbInfo(sql)
			data = data.fillna(0)
			repay = pd.merge(alldata,data)
			pp.append(pd.Series([round(x*100,2) for x in (repay['allPayMoney']-repay['payMoney'])/repay['allMoney']],index=repay['date']))

		pt = pd.concat(pp, axis=1, join_axes=[pp[0].index])
		pt.columns = ['首逾率','逾期率3+','逾期率7+','逾期率10+','逾期率20+','逾期率M1','逾期率M2','逾期率M3']
		pt = pt.fillna(0)
		pt['times'] = list(pt.index)

		s0 = list(pt['首逾率'])
		s3 = list(pt['逾期率3+'])
		s7 = list(pt['逾期率7+'])
		s10 = list(pt['逾期率10+'])
		s20 = list(pt['逾期率20+'])
		sM1 = list(pt['逾期率M1'])
		sM2 = list(pt['逾期率M2'])
		sM3 = list(pt['逾期率M3'])
		stt = list(pt['times'])
		fnanme = [fundName] * len(pt)

		sql = "delete from dayAddApi_FlowDelayRate where fundName='" + fundName + "'"
		status = pysql.deletetData(sql)
		log.log(u'逾期数据删除状态-{}！(资金方{})'.format(status,fundName),'info')

		sql = """ insert into dayAddApi_FlowDelayRate(fundName,delayRate0,delayRate3,delayRate7,delayRate10,delayRate20,delayRateM1,delayRateM2,delayRateM3,createDate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
		dset = zip(fnanme,s0,s3,s7,s10,s20,sM1,sM2,sM3,stt)
		status = pysql.insertData(sql,dset)
		log.log(u'逾期数据更新状态-{}！(资金方{})'.format(status,fundName),'info')

#逾期情况 分新老 根据资金方区分
def delayDayNOFund():
	fundId = config.fundloanId
	for fundName in fundId.keys():
		ids = fundId[fundName][0]

		timeList = timeScale('2017-08-30')[:-3]
		sql = "select distinct createDate from dayAddApi_FlowDelayRateNO where fundName='" + fundName + "'";
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

			print u'逾期(新老)3天逾期率' + fundName + ' ' + stTime

			#分新老首逾情况
			#new
			sql = """
				select sum(b.repayMoney+b.overdueInterest+b.overdueFee),sum(a.payMoney)
				from loan a,loan_repaying b 
				where a.id=b.loanId and a.status=6 and b.compatibleStatus not in ('UNPAID','CANCEL') and b.productId not in (3,4,5,6,1001)
				and b.termDate >= '{}' and b.termDate < '{}'
				and a.userSid not in (select distinct userSid from loan_repaying where termDate < '{}')
				and a.fundPayAccountId in ({})
			""".format(stTime,edTime,stTime,ids)
			data = pysql.dbInfo(sql)
			data = data.fillna(0)
			newRepaySum = data.values[0][0]
			newPaySum = data.values[0][1]

			sql = """
				select sum(a.payMoney)
				from loan a,loan_repaying b 
				where a.id=b.loanId and a.status=6 and b.compatibleStatus not in ('UNPAID','CANCEL') and b.productId not in (3,4,5,6,1001)
				and b.termDate >= '{}' and b.termDate < '{}' 
				and if(b.repaidTime is NULL,TO_DAYS(now()) - TO_DAYS(b.termDate),TO_DAYS(b.repaidTime) - TO_DAYS(b.termDate)) <= 3
				and a.userSid not in (
				select distinct userSid from loan_repaying where termDate < '{}'
				)
				and a.fundPayAccountId in ({})
			""".format(stTime,edTime,stTime,ids)
			data = pysql.dbInfo(sql)
			data = data.fillna(0)
			newPaid = data.values[0][0]
			newDelayRate = round((newPaySum - newPaid)/newRepaySum*100,2)
			#old
			sql = """
				select sum(b.repayMoney+b.overdueInterest+b.overdueFee),sum(a.payMoney)
				from loan a,loan_repaying b 
				where a.id=b.loanId and a.status=6 and b.compatibleStatus not in ('UNPAID','CANCEL') and b.productId not in (3,4,5,6,1001)
				and b.termDate >= '{}' and b.termDate < '{}' 
				and a.userSid in (
				select distinct userSid from loan_repaying where termDate < '{}'
				)
				and a.fundPayAccountId in ({})
			""".format(stTime,edTime,stTime,ids)
			data = pysql.dbInfo(sql)
			data = data.fillna(0)
			oldRepaySum = data.values[0][0]
			oldPaySum = data.values[0][1]
			sql = """
				select sum(a.payMoney)
				from loan a,loan_repaying b 
				where a.id=b.loanId and a.status=6 and b.compatibleStatus not in ('UNPAID','CANCEL') and b.productId not in (3,4,5,6,1001)
				and b.termDate >= '{}' and b.termDate < '{}' 
				and if(b.repaidTime is NULL,TO_DAYS(now()) - TO_DAYS(b.termDate),TO_DAYS(b.repaidTime) - TO_DAYS(b.termDate)) <= 3
				and a.userSid in (
				select distinct userSid from loan_repaying where termDate < '{}'
				)
				and a.fundPayAccountId in ({})
			""".format(stTime,edTime,stTime,ids)
			data = pysql.dbInfo(sql)
			data = data.fillna(0)
			oldPaid = data.values[0][0]
			oldDelayRate = round((oldPaySum - oldPaid)/oldRepaySum*100,2)

			sql = """ insert into dayAddApi_FlowDelayRateNO(fundName,newPaySum,newRepaySum,newPaid,newDelayRate3,oldPaySum,oldRepaySum,oldPaid,oldDelayRate3,createDate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
			dset = [(fundName,newPaySum,newRepaySum,newPaid,newDelayRate,oldPaySum,oldRepaySum,oldPaid,oldDelayRate,stTime)]
			status = pysql.insertData(sql,dset)
			log.log(u'逾期3天(新老)数据更新状态-{}！({})(资金方{})！'.format(status,stTime,fundName),'info')

def main():
	delayDayFund()
	delayDayNOFund()
	
def strtotime(strtime):
    if type(strtime) in [pd.tslib.NaTType]:
        strtime = datetime.datetime.now()
    return strtime
 
if __name__ == '__main__':
	main()

