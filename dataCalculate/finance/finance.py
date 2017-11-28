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

from libfile import pysql
from libfile import logger
import config

reload(sys)   
sys.setdefaultencoding('utf-8')

#日志
log = logger.Logger('index',os.path.abspath(os.path.dirname(__file__)) + "/" + config.log_path)

#路径
def getTheFile(filename):
    return os.path.abspath(os.path.dirname(__file__)) +"/"+filename

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

def todayLoan():
	fundloan = {
		u'快乐达连连账户':['10001'],
		u'纵横新创30':['10002'],
		u'纵横新创14':['10004'],
		u'口袋理财v2':['10003'],
		u'柚子理财':['10005'],
		u'魔贷金融1':['10006'],
		u'魔贷金融2':['10010'],
		u'小袋理财':['10007'],
		u'爱多贷':['10008'],
		# u'暴雷科技':['10009'],
		u'拿点花':['10011'],
		u'付呗零用钱':['10012'],
		u'星火钱包1':['20001'],
		u'星火钱包2':['20002'],
		u'魔贷资金资产':['10017'],
		u'钱好借':['10016'],
		u'速融超':['10015'],
		# u'小桥钱包':['10014'],
		u'有钱来了':['10013'],
		u'借袋钱':['10019'],
		u'点点花':['10020'],
	}
	fundloanToday = {'fundId':{}}
	for key in fundloan.keys():
		fundId = "','".join(fundloan[key])
		sql = """
			select sum(payMoney) from loan where status=6 and fundPayAccountId='{}' and createdTime >= DATE_FORMAT(NOW(),'%Y-%m-%d')
		""".format(fundId)
		data = getdata(sql)
		data = data.fillna(0)
		fundloanToday['fundId'][key] = int(data.values[0][0])
	fundloanToday['paidAll'] = intothousand(numpy.sum(fundloanToday['fundId'].values()))
	return fundloanToday

def todayLoanDetail():
	loanDetail = {}
	hours = []
	cumMoney = []
	sql = """
		select DATE_FORMAT(createdTime,'%H') 'hour',sum(payMoney) 'loanMoney' from loan 
		where status=6 and createdTime >= DATE_FORMAT(NOW(),'%Y-%m-%d')
		group by DATE_FORMAT(createdTime,'%H')
	"""
	data = getdata(sql)
	data = data.fillna(0)
	for i in range(len(data)):
		hours.append(data['hour'][i])
		cumMoney.append(int(numpy.sum(data['loanMoney'][:i+1])))
	loanDetail['hours'] = hours
	loanDetail['cumMoney'] = cumMoney
	return json.dumps(loanDetail, default=config.set_default)

def main():
	todayLoan()
	todayLoanDetail()

def getdata(sql):
	data = pd.DataFrame()
	try:
		conn = pysql.conn_mysql()
		data = pd.read_sql_query(sql,con = conn)
		conn.close()
	except MySQLdb.Error,e:
		log.log('数据库链接错误！','warning')

	return data
 

if __name__ == '__main__':
	main()

