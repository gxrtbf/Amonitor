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

from libfile import pysql
from libfile import logger
import config

reload(sys)   
sys.setdefaultencoding('utf-8')

log = logger.Logger('aeye', os.path.abspath(os.path.dirname(__file__)) + "/" + config.log_path)

#路径
def getTheFile(filename):
    return os.path.abspath(os.path.dirname(__file__)) +"/"+filename

#数据包含时间
def timeScale(startTime=None):
	if startTime is None:
		startTime = "2017-03-01"
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

#dataframe变成dict
def df2dict(df):
	djson = {}
	for key in df.columns:
			djson[key] = list(df[key])
	return djson

#可加性dict
def df2dict2(df,title,num):
	djson = {}
	for i in range(len(df)):
		djson[df.iloc[i][title]] = df.iloc[i][num]
	return djson

#数字生成千分位
def intothousand(num):
	strn = []
	n = 5 
	while n > 0:
		n = n - 1
		if num < 1000**n:
			continue
		st = int(num/1000**n)
		num = num - st*1000**n
		if len(strn) == 0:
			strn.append(str(st))
		else:
			strn.append('0'*(3-len(str(st))) + str(st))
		if num < 1000:
			strn.append('0'*(3-len(str(num))) + str(num))
			break
	ss = ','.join(strn)
	return ss

#模型基本情况
def modelCheck():
	if not os.path.exists(getTheFile('../static/data/aeye/modelCheck.json')):
		json.dump({'trend':{'times':[]}}, open(getTheFile('../static/data/aeye/modelCheck.json'), 'w'), default=config.set_default)
	check_dict = json.load(open(getTheFile('../static/data/aeye/modelCheck.json')))

	timeList = timeScale('2017-08-24')
	for i in range(len(timeList)-1):
		stTime = timeList[i]
		edTime = timeList[i+1]

		if stTime in check_dict['trend'].keys():
			continue	
		#审核情况
		sql = """
			select policyResult,credanScore1Result,blacklist1Result,credanScore2Result,blacklist2Result,xiguafenResult,auditResult,date_format(created_time,'%Y-%m-%d') 'date' 
			from batch_auto_audit_score where created_time >= '{}' and created_time < '{}';
		""".format(stTime,edTime)
		data = user_info(sql)

		if data.empty:
			continue

		check_dict['trend'][stTime] = {}	
		print '模型审核数据更新:' + stTime
		#每日审核量
		check_dict['trend'][stTime]['dayCheck'] = len(data)
		#每日通过量
		check_dict['trend'][stTime]['dayPass'] = numpy.sum(data['auditResult']==1)
		#每日拒绝量
		check_dict['trend'][stTime]['dayReject'] = numpy.sum(data['auditResult']==4)
		#通过率
		check_dict['trend'][stTime]['passRate'] = check_dict['trend'][stTime]['dayPass']/float(check_dict['trend'][stTime]['dayCheck'])
		check_dict['trend'][stTime]['passRate'] = round(check_dict['trend'][stTime]['passRate'] * 100,2)
		
		check_dict['trend']['times'].append(stTime)
		check_dict['trend']['times'] = sorted(set(check_dict['trend']['times']))
		json.dump(check_dict, open(getTheFile('../static/data/flow/modelCheck.json'), 'w'), default=config.set_default)
		log.log('审核模型数据更新完成({})！'.format(stTime),'info')

	#各原因拒绝量
	sql = """
		select policyResult,credanScore1Result,blacklist1Result,credanScore2Result,blacklist2Result,xiguafenResult,auditResult
		from batch_auto_audit_score
		where DATE_SUB(CURDATE(), INTERVAL 1 MONTH) <= created_time and auditResult=4;
	"""
	temp = user_info(sql)
	policyReject = numpy.sum(temp['policyResult']==4)
	credanScore1Result = numpy.sum(temp['credanScore1Result']==4)
	blacklist1Result = numpy.sum(temp['blacklist1Result']==4)
	credanScore2Result = numpy.sum(temp['credanScore2Result']==4)
	blacklist2Result = numpy.sum(temp['blacklist2Result']==4)
	xiguafenResult = numpy.sum(temp['xiguafenResult']==4)
	#拒绝量分布
	temp['h4'] = (temp['policyResult']==4).map(int)+ (temp['credanScore1Result']==4).map(int)+ (temp['blacklist1Result']==4).map(int)+ (temp['credanScore2Result']==4).map(int)+ (temp['blacklist2Result']==4).map(int)+ (temp['xiguafenResult']==4).map(int)
	temp["数量"] = 1 
	temp10 = pd.pivot_table(temp,index=["h4"],values=["数量"],aggfunc='sum',fill_value=0)
	#单独拒绝量
	tempp = temp[temp['h4']==1]
	tpolicyReject = numpy.sum(tempp['policyResult']==4)
	tcredanScore1Result = numpy.sum(tempp['credanScore1Result']==4)
	tblacklist1Result = numpy.sum(tempp['blacklist1Result']==4)
	tcredanScore2Result = numpy.sum(tempp['credanScore2Result']==4)
	tblacklist2Result = numpy.sum(tempp['blacklist2Result']==4)
	txiguafenResult = numpy.sum(tempp['xiguafenResult']==4)

	#总量情况
	check_dict['all'] = {}
	sql = """
		select count(*) from batch_auto_audit_score
	"""
	data = user_info(sql)
	data = data.fillna(0)
	check_dict['all']['allCheck'] = {}
	check_dict['all']['allCheck']['value'] = data.values[0][0]
	check_dict['all']['allCheck']['label'] = intothousand(data.values[0][0])
	sql = """
		select count(*) from batch_auto_audit_score where auditResult=1
	"""
	data = user_info(sql)
	data = data.fillna(0)
	check_dict['all']['allPass'] = {}
	check_dict['all']['allPass']['value'] = data.values[0][0]
	check_dict['all']['allPass']['label'] = intothousand(data.values[0][0])
	sql = """
		select count(*) from batch_auto_audit_score where auditResult=4
	"""
	data = user_info(sql)
	data = data.fillna(0)
	check_dict['all']['allReject'] = {}
	check_dict['all']['allReject']['value'] = data.values[0][0]
	check_dict['all']['allReject']['label'] = intothousand(data.values[0][0])

	check_dict['all']['passRate'] = round(check_dict['all']['allPass']['value']/float(check_dict['all']['allCheck']['value'])*100,2)

	check_dict['label'] = ['政策','score1','blacklist1','score2','blacklist2','西瓜分']
	check_dict['reject'] = [policyReject,credanScore1Result,blacklist1Result,credanScore2Result,blacklist2Result,xiguafenResult]
	check_dict['rejectOnly'] = [tpolicyReject,tcredanScore1Result,tblacklist1Result,tcredanScore2Result,tblacklist2Result,txiguafenResult]
	check_dict['rejectDis'] = {}
	check_dict['rejectDis']['label'] = list(temp10.index)
	check_dict['rejectDis']['value'] = list(temp10['数量'])

	json.dump(check_dict, open(getTheFile('../static/data/aeye/modelCheck.json'), 'w'), default=config.set_default)
	log.log('审核所有数据更新完成({})！'.format(stTime),'info')

#逾期情况
def delayDay():
	#逾期情况 not in (3,4,5,6,1001)
	sql = """
		select DATE_FORMAT(b.termDate,'%Y-%m-%d') 'date',sum(a.payMoney) 'allPayMoney',sum(b.repayMoney+b.overdueInterest+b.overdueFee) 'allMoney' from loan a,loan_repaying b 
		where a.id=b.loanId and a.status=6 and b.compatibleStatus not in ('UNPAID','CANCEL') and b.productId not in (3,4,5,6,1001)
		and b.termDate < DATE_FORMAT(now(),'%Y-%m-%d')
		GROUP BY DATE_FORMAT(b.termDate,'%Y-%m-%d');
	"""
	alldata = user_info(sql)
	delayPoint = [0,3,7,10,20,30,60,90]
	pp = []
	for day in delayPoint:
		sql = """
			select DATE_FORMAT(c.termDate,'%Y-%m-%d') 'date',sum(c.payMoney) 'payMoney' from (
			select a.payMoney,b.* from loan a,loan_repaying b 
			where a.id=b.loanId and a.status=6 and b.compatibleStatus not in ('UNPAID','CANCEL') and b.productId not in (3,4,5,6,1001)
			and b.termDate < DATE_FORMAT(now(),'%Y-%m-%d')
			HAVING if(b.repaidTime is NULL,TO_DAYS(now()) - TO_DAYS(b.termDate),TO_DAYS(b.repaidTime) - TO_DAYS(b.termDate)) <= {}) c
			GROUP BY DATE_FORMAT(c.termDate,'%Y-%m-%d');
		""".format(day)
		plan = user_info(sql)

		repay = pd.merge(alldata,plan)
		pp.append(pd.Series([round(x*100,2) for x in (repay['allPayMoney']-repay['payMoney'])/repay['allMoney']],index=repay['date']))
	pt = pd.concat(pp, axis=1, join_axes=[pp[0].index])
	pt.columns = ['首逾率','逾期率3+','逾期率7+','逾期率10+','逾期率20+','逾期率M1','逾期率M2','逾期率M3']
	pt = pt.fillna(0)
	pt['times'] = list(pt.index)

	pt_json = {}
	pt_json['label'] = ['首逾率','逾期率3+','逾期率7+','逾期率10+','逾期率20+','逾期率M1','逾期率M2','逾期率M3']
	pt_json['trend'] = df2dict(pt)

	json.dump(pt_json, open(getTheFile('../static/data/aeye/delayDay.json'), 'w'), default=config.set_default)
	log.log('逾期数据更新完成！','info')

#逾期情况（新老）
def delayDayNO():
	if not os.path.exists(getTheFile('../static/data/aeye/delayDayNO.json')):
		json.dump({'trend':{},'times':[]}, open(getTheFile('../static/data/aeye/delayDayNO.json'), 'w'), default=config.set_default)
	delayDayNO = json.load(open(getTheFile('../static/data/aeye/delayDayNO.json')))

	timeList = timeScale()[:-3]
	for i in range(len(timeList)-1):
		stTime = timeList[i]
		edTime = timeList[i+1]

		if stTime in delayDayNO['trend'].keys():
			continue
		print '逾期(新老)3天逾期率' + stTime
		delayDayNO['trend'][stTime] = {}
		#不分新老首逾情况
		# sql = """
		# 	select sum(a.payMoney)
		# 	from loan a,loan_repaying b 
		# 	where a.id=b.loanId and a.status=6 and b.compatibleStatus not in ('UNPAID','CANCEL') 
		# 	and b.termDate >= '{}' and b.termDate < '{}';
		# """.format(stTime,edTime)
		# data = user_info(sql)
		# data = data.fillna(0)
		# delayDayNO['trend'][stTime]['all'] = {}
		# delayDayNO['trend'][stTime]['all']['sum'] = data.values[0][0]

		# sql = """
		# 	select sum(a.payMoney)
		# 	from loan a,loan_repaying b 
		# 	where a.id=b.loanId and a.status=6 and b.compatibleStatus not in ('UNPAID','CANCEL') 
		# 	and b.termDate >= '{}' and b.termDate < '{}' and DATE_FORMAT(b.termDate,'%Y-%m-%d') >= DATE_FORMAT(b.repaidTime,'%Y-%m-%d');
		# """.format(stTime,edTime)
		# data = user_info(sql)
		# data = data.fillna(0)
		# delayDayNO['trend'][stTime]['all']['pay'] = data.values[0][0]
		# delayDayNO['trend'][stTime]['all']['delayRate'] = 100 - round(delayDayNO['trend'][stTime]['all']['pay']/float(delayDayNO['trend'][stTime]['all']['sum'])*100,2)

		#分新老首逾情况
		#new
		sql = """
			select sum(b.repayMoney+b.overdueInterest+b.overdueFee),sum(a.payMoney)
			from loan a,loan_repaying b 
			where a.id=b.loanId and a.status=6 and b.compatibleStatus not in ('UNPAID','CANCEL') and b.productId not in (3,4,5,6,1001)
			and b.termDate >= '{}' and b.termDate < '{}'
			and a.userSid not in (select distinct userSid from loan_repaying where termDate < '{}')
		""".format(stTime,edTime,stTime)
		data = user_info(sql)
		data = data.fillna(0)
		delayDayNO['trend'][stTime]['new'] = {}
		delayDayNO['trend'][stTime]['new']['repaySum'] = data.values[0][0]
		delayDayNO['trend'][stTime]['new']['paySum'] = data.values[0][1]

		sql = """
			select sum(a.payMoney)
			from loan a,loan_repaying b 
			where a.id=b.loanId and a.status=6 and b.compatibleStatus not in ('UNPAID','CANCEL') and b.productId not in (3,4,5,6,1001)
			and b.termDate >= '{}' and b.termDate < '{}' 
			and if(b.repaidTime is NULL,TO_DAYS(now()) - TO_DAYS(b.termDate),TO_DAYS(b.repaidTime) - TO_DAYS(b.termDate)) <= 3
			and a.userSid not in (
  				select distinct userSid from loan_repaying where termDate < '{}'
			);
		""".format(stTime,edTime,stTime)
		data = user_info(sql)
		data = data.fillna(0)
		delayDayNO['trend'][stTime]['new']['paid'] = data.values[0][0]
		delayDayNO['trend'][stTime]['new']['delayRate'] = round((delayDayNO['trend'][stTime]['new']['paySum'] - delayDayNO['trend'][stTime]['new']['paid'])/delayDayNO['trend'][stTime]['new']['repaySum']*100,2)
		#old
		sql = """
			select sum(b.repayMoney+b.overdueInterest+b.overdueFee),sum(a.payMoney)
			from loan a,loan_repaying b 
			where a.id=b.loanId and a.status=6 and b.compatibleStatus not in ('UNPAID','CANCEL') and b.productId not in (3,4,5,6,1001)
			and b.termDate >= '{}' and b.termDate < '{}' 
			and a.userSid in (
  				select distinct userSid from loan_repaying where termDate < '{}'
			);
		""".format(stTime,edTime,stTime)
		data = user_info(sql)
		data = data.fillna(0)
		delayDayNO['trend'][stTime]['old'] = {}
		delayDayNO['trend'][stTime]['old']['repaySum'] = data.values[0][0]
		delayDayNO['trend'][stTime]['old']['paySum'] = data.values[0][1]
		sql = """
			select sum(a.payMoney)
			from loan a,loan_repaying b 
			where a.id=b.loanId and a.status=6 and b.compatibleStatus not in ('UNPAID','CANCEL') and b.productId not in (3,4,5,6,1001)
			and b.termDate >= '{}' and b.termDate < '{}' 
			and if(b.repaidTime is NULL,TO_DAYS(now()) - TO_DAYS(b.termDate),TO_DAYS(b.repaidTime) - TO_DAYS(b.termDate)) <= 3
			and a.userSid in (
  				select distinct userSid from loan_repaying where termDate < '{}'
			);
		""".format(stTime,edTime,stTime)
		data = user_info(sql)
		data = data.fillna(0)
		delayDayNO['trend'][stTime]['old']['paid'] = data.values[0][0]
		delayDayNO['trend'][stTime]['old']['delayRate'] = round((delayDayNO['trend'][stTime]['old']['paySum'] - delayDayNO['trend'][stTime]['old']['paid'])/delayDayNO['trend'][stTime]['old']['repaySum']*100,2)
		
		delayDayNO['times'].append(stTime)
		delayDayNO['times'] = sorted(set(delayDayNO['times']))
		json.dump(delayDayNO, open(getTheFile('../static/data/aeye/delayDayNO.json'), 'w'), default=config.set_default)
		log.log('逾期3天(新老)数据更新完成({})！'.format(stTime),'info')

#逾期情况 根据资金方区分
def delayDayFund():
	fundId = config.fundloanId
	delayDayFund = {}
	for fundName in fundId.keys():
		print fundName
		ids = fundId[fundName][0]
		#逾期情况 not in (3,4,5,6,1001)
		sql = """
			select DATE_FORMAT(b.termDate,'%Y-%m-%d') 'date',sum(a.payMoney) 'allPayMoney',sum(b.repayMoney+b.overdueInterest+b.overdueFee) 'allMoney' from loan a,loan_repaying b 
			where a.id=b.loanId and a.status=6 and b.compatibleStatus not in ('UNPAID','CANCEL') and a.fundPayAccountId in ({})
			and b.productId not in (3,4,5,6,1001)
			and b.termDate < DATE_FORMAT(now(),'%Y-%m-%d')
			GROUP BY DATE_FORMAT(b.termDate,'%Y-%m-%d');
		""".format(ids)
		alldata = user_info(sql)
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
			plan = user_info(sql)

			repay = pd.merge(alldata,plan)
			pp.append(pd.Series([round(x*100,2) for x in (repay['allPayMoney']-repay['payMoney'])/repay['allMoney']],index=repay['date']))
		pt = pd.concat(pp, axis=1, join_axes=[pp[0].index])
		pt.columns = ['首逾率','逾期率3+','逾期率7+','逾期率10+','逾期率20+','逾期率M1','逾期率M2','逾期率M3']
		pt = pt.fillna(0)
		pt['times'] = list(pt.index)

		pt_json = {}
		pt_json['label'] = ['首逾率','逾期率3+','逾期率7+','逾期率10+','逾期率20+','逾期率M1','逾期率M2','逾期率M3']
		pt_json['trend'] = df2dict(pt)

		delayDayFund[fundName] = pt_json

		json.dump(delayDayFund, open(getTheFile('../static/data/aeye/delayDayFund.json'), 'w'), default=config.set_default)
	log.log('逾期数据更新完成！(资金方{})'.format(fundName),'info')

#逾期情况 分新老 根据资金方区分
def delayDayNOFund():
	if not os.path.exists(getTheFile('../static/data/aeye/delayDayNOFund.json')):
		json.dump({}, open(getTheFile('../static/data/aeye/delayDayNOFund.json'), 'w'), default=config.set_default)
	delayDayNOFund = json.load(open(getTheFile('../static/data/aeye/delayDayNOFund.json')))

	fundId = config.fundloanId
	for fundName in fundId.keys():
		ids = fundId[fundName][0]
		if not delayDayNOFund.get(fundName,''):
			delayDayNOFund[fundName] = {'trend':{},'times':[]}
		temp = delayDayNOFund[fundName]

		timeList = timeScale('2017-08-30')[:-3]
		for i in range(len(timeList)-1):
			stTime = timeList[i]
			edTime = timeList[i+1]

			if stTime in temp['trend'].keys():
				continue
			print '逾期(新老)3天逾期率' + fundName + ' ' + stTime
			temp['trend'][stTime] = {}

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
			data = user_info(sql)
			data = data.fillna(0)
			temp['trend'][stTime]['new'] = {}
			temp['trend'][stTime]['new']['repaySum'] = data.values[0][0]
			temp['trend'][stTime]['new']['paySum'] = data.values[0][1]

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
			data = user_info(sql)
			data = data.fillna(0)
			temp['trend'][stTime]['new']['paid'] = data.values[0][0]
			temp['trend'][stTime]['new']['delayRate'] = round((temp['trend'][stTime]['new']['paySum'] - temp['trend'][stTime]['new']['paid'])/temp['trend'][stTime]['new']['repaySum']*100,2)
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
			data = user_info(sql)
			data = data.fillna(0)
			temp['trend'][stTime]['old'] = {}
			temp['trend'][stTime]['old']['repaySum'] = data.values[0][0]
			temp['trend'][stTime]['old']['paySum'] = data.values[0][1]
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
			data = user_info(sql)
			data = data.fillna(0)
			temp['trend'][stTime]['old']['paid'] = data.values[0][0]
			temp['trend'][stTime]['old']['delayRate'] = round((temp['trend'][stTime]['old']['paySum'] - temp['trend'][stTime]['old']['paid'])/temp['trend'][stTime]['old']['repaySum']*100,2)
			
			temp['times'].append(stTime)
			temp['times'] = sorted(set(temp['times']))
			delayDayNOFund[fundName] = temp
			json.dump(delayDayNOFund, open(getTheFile('../static/data/aeye/delayDayNOFund.json'), 'w'), default=config.set_default)
			log.log('逾期3天(新老)数据更新完成({})(资金方{})！'.format(stTime,fundName),'info')

def mutiLoan():
	wd = 'C:/Users/Amon/Desktop/save_data/jsonData'
	#wd = '/root/Credan/Mmodel/save_data'
	if not os.path.exists(getTheFile('../static/data/aeye/mutiloan.json')):
		json.dump({'trend':{},'times':[]}, open(getTheFile('../static/data/aeye/mutiloan.json'), 'w'), default=config.set_default)
	mutiloan = json.load(open(getTheFile('../static/data/aeye/mutiloan.json')))
	today = str(datetime.datetime.now().date())
	for date in sorted(os.listdir(wd)):
		if date == today:
			continue 
		if mutiloan['trend'].get(date):
			continue
		print date
		dir_path = wd + '/' + date
		file_paths = [dir_path + '/' + file for file in os.listdir(dir_path)]
		contacting_xj_num = []
		contacted_xj_num = []
		for file in file_paths:
			print file
			jd = json.load(open(file))
			if type(jd) not in [dict]:
				jd = eval(jd)
			contacting_xj_num.append(jd.get('contacting_xj_num',0))
			contacted_xj_num.append(jd.get('contacted_xj_num',0))
		#平均值	
		mn_contacting_xj_num = numpy.mean(contacting_xj_num)
		mn_contacted_xj_num = numpy.mean(contacted_xj_num)
		#中位数
		md_contacting_xj_num = numpy.median(contacting_xj_num)
		md_contacted_xj_num = numpy.median(contacted_xj_num)
			
		binss = [-1,0,3,8,13,20,max(contacting_xj_num + contacted_xj_num)+200]
		llables = ['0','1-3','4-8','9-13','14-20','21-']
		contacting = pd.cut(contacting_xj_num,bins=binss,labels=llables).value_counts()/len(contacting_xj_num)
		contacted = pd.cut(contacted_xj_num,bins=binss,labels=llables).value_counts()/len(contacted_xj_num)
		#生成json
		pJson = {}
		pJson['contacting'] = {}
		pJson['contacting']['percent'] = [round(contacting.ix[x]*100,2) for x in llables]
		pJson['contacting']['mean'] = round(mn_contacting_xj_num,2)
		pJson['contacting']['median'] = round(md_contacting_xj_num,2)
		pJson['contacting']['count'] = len(contacting_xj_num)

		pJson['contacted'] = {}
		pJson['contacted']['percent'] = [round(contacted.ix[x]*100,2) for x in llables]
		pJson['contacted']['mean'] = round(mn_contacted_xj_num,2)
		pJson['contacted']['median'] = round(md_contacted_xj_num,2)
		pJson['contacted']['count'] = len(contacted_xj_num)

		mutiloan['trend'][date] = pJson
		mutiloan['times'].append(date)

	mutiloan['sum'] = {}
	mutiloan['sum']['label'] = ['0','1-3','4-8','9-13','14-20','21-']
	sumcontacting = [0,0,0,0,0,0]
	sumcontacted = [0,0,0,0,0,0]
	for key in mutiloan['trend'].keys():
		for i in range(6):
			sumcontacting[i] += mutiloan['trend'][key]['contacting']['percent'][i]*mutiloan['trend'][key]['contacting']['count']
			sumcontacted[i] += mutiloan['trend'][key]['contacted']['percent'][i]*mutiloan['trend'][key]['contacted']['count']
	mutiloan['sum']['contacting'] = sumcontacting
	mutiloan['sum']['contacted'] = sumcontacted
	json.dump(mutiloan, open(getTheFile('../static/data/aeye/mutiLoan.json'), 'w'), default=config.set_default)
	log.log('多头数据更新完成！','info')

def main():
	#modelCheck()
	#delayDay()
	#delayDayNO()
	#delayDayFund()
	delayDayNOFund()
	#mutiLoan()
	

def strtotime(strtime):
    if type(strtime) in [pd.tslib.NaTType]:
        strtime = datetime.datetime.now()
    return strtime

def user_info(sql):
	data = pd.DataFrame()
	try:
		conn = pysql.conn_mysql()
		data = pd.read_sql_query(sql,con = conn)
		conn.close()
	except MySQLdb.Error,e:
		logging.warning("user_info: Mysql Error %d: %s" % (e.args[0], e.args[1]))

	return data
 
if __name__ == '__main__':
	main()

