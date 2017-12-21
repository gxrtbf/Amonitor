# -*- coding: utf-8 -*-
from django.db import models
import django.utils.timezone as timezone

#index
class IndexHead(models.Model):
	tradeMoney = models.IntegerField(default=0)
	tradeNum = models.IntegerField(default=0)
	activeUser = models.IntegerField(default=0)
	sumUser = models.IntegerField(default=0)
	createDate = models.DateField(primary_key=True,default=timezone.now)

	class Meta:
		ordering = ('createDate',)

class IndexDash(models.Model):
	avgTermNum = models.IntegerField(default=0)
	avgMoney = models.IntegerField(default=0)
	avgServiceMoney = models.IntegerField(default=0)
	createDate = models.DateField(primary_key=True,default=timezone.now)

	class Meta:
		ordering = ('createDate',)

class IndexHopper(models.Model):
	register = models.IntegerField(default=0)
	applys = models.IntegerField(default=0)
	passs = models.IntegerField(default=0)
	loan = models.IntegerField(default=0)
	reloan = models.IntegerField(default=0)
	createDate = models.DateField(primary_key=True,default=timezone.now)

	class Meta:
		ordering = ('createDate',)

class IndexCity(models.Model):
	cityName = models.CharField(max_length=32,default='china')
	numInCity = models.IntegerField(default=0)
	createDate = models.DateField(default=timezone.now)

	class Meta:
		ordering = ('createDate',)

	unique_together = ('cityName', 'createDate')


class IndexAcrepay(models.Model):
	allRepayMoney = models.IntegerField(default=0)
	acRepayMoney = models.IntegerField(default=0)
	repayRate = models.IntegerField(default=0)
	createDate = models.DateField(primary_key=True,default=timezone.now)

	class Meta:
		ordering = ('createDate',)

#userInfo
class UserAge(models.Model):
	age1 = models.IntegerField(default=0)
	age2 = models.IntegerField(default=0)
	age3 = models.IntegerField(default=0)
	age4 = models.IntegerField(default=0)
	age5 = models.IntegerField(default=0)
	createDate = models.DateField(primary_key=True,default=timezone.now)

	class Meta:
		ordering = ('createDate',)

class UserAgeAll(models.Model):
	age1 = models.IntegerField(default=0)
	age2 = models.IntegerField(default=0)
	age3 = models.IntegerField(default=0)
	age4 = models.IntegerField(default=0)
	age5 = models.IntegerField(default=0)
	createDate = models.DateField(primary_key=True,default=timezone.now)

	class Meta:
		ordering = ('createDate',)

class UserSex(models.Model):
	male = models.IntegerField(default=0)
	female = models.IntegerField(default=0)
	createDate = models.DateField(primary_key=True,default=timezone.now)

	class Meta:
		ordering = ('createDate',)

class UserSexAll(models.Model):
	male = models.IntegerField(default=0)
	female = models.IntegerField(default=0)
	createDate = models.DateField(primary_key=True,default=timezone.now)

	class Meta:
		ordering = ('createDate',)

class UserIncrease(models.Model):
	register = models.IntegerField(default=0)
	allow = models.IntegerField(default=0)
	newApply = models.IntegerField(default=0)
	oldApply = models.IntegerField(default=0)
	createDate = models.DateField(primary_key=True,default=timezone.now)

	class Meta:
		ordering = ('createDate',)

class UserRest(models.Model):
	registerDate = models.CharField(max_length=32,default='2017-12')
	currentDate = models.CharField(max_length=32,default='2017-12')
	allPass = models.IntegerField(default=0)
	currentActive = models.IntegerField(default=0)
	currentActiveRate = models.FloatField(default=0.0)
	createDate = models.DateField(default=timezone.now)

	class Meta:
		ordering = ('registerDate', 'currentDate',)

	unique_together = ('registerDate', 'currentDate')

#flow
class FlowLoanMoney(models.Model):
	product = models.CharField(max_length=32,default='flash')
	money = models.IntegerField(default=0)
	createDate = models.DateField(default=timezone.now)

	class Meta:
		ordering = ('createDate',)

	unique_together = ('product', 'createDate')

class FlowLoanMoneyNO(models.Model):
	loanOld = models.IntegerField(default=0)
	loanNew = models.IntegerField(default=0)
	createDate = models.DateField(primary_key=True,default=timezone.now)

	class Meta:
		ordering = ('createDate',)

class FlowLoanMoneySum(models.Model):
	product = models.CharField(max_length=32,default='flash')
	money = models.IntegerField(default=0)
	createDate = models.DateField(default=timezone.now)

	class Meta:
		ordering = ('createDate',)

	unique_together = ('product', 'createDate')

class FlowPaidMoney(models.Model):
	paidMoney = models.IntegerField(default=0)
	createDate = models.DateField(primary_key=True,default=timezone.now)

	class Meta:
		ordering = ('createDate',)

class FlowDelayRate(models.Model):
	fundName = models.CharField(max_length=128,default='credan')
	delayRate0 = models.FloatField(default=0.0)
	delayRate3 = models.FloatField(default=0.0)
	delayRate7 = models.FloatField(default=0.0)
	delayRate10 = models.FloatField(default=0.0)
	delayRate20 = models.FloatField(default=0.0)
	delayRateM1 = models.FloatField(default=0.0)
	delayRateM2 = models.FloatField(default=0.0)
	delayRateM3 = models.FloatField(default=0.0)
	createDate = models.DateField(default=timezone.now)

	class Meta:
		ordering = ('createDate',)

	unique_together = ('fundName', 'createDate')

class FlowDelayRateNO(models.Model):
	fundName = models.CharField(max_length=128,default='credan')
	newDelayRate3 = models.FloatField(default=0.0)
	newRepaySum = models.IntegerField(default=0)
	newPaid = models.IntegerField(default=0)
	oldDelayRate3 = models.FloatField(default=0.0)
	oldRepaySum = models.IntegerField(default=0)
	oldPaid = models.IntegerField(default=0)
	createDate = models.DateField(default=timezone.now)

	class Meta:
		ordering = ('createDate',)

	unique_together = ('fundName', 'createDate')

class FlowLoanFund(models.Model):
	fundName = models.CharField(max_length=128,default='credan')
	sumMoney = models.FloatField(default=0.0)
	createDate = models.DateField(default=timezone.now)

	class Meta:
		ordering = ('createDate',)

	unique_together = ('fundName', 'createDate')

#collect

class CollectRate(models.Model):
	month = models.CharField(max_length=128,default='2017-04')
	day4Rate = models.FloatField(default=0.0)
	day7Rate = models.FloatField(default=0.0)
	day15Rate = models.FloatField(default=0.0)
	day30Rate = models.FloatField(default=0.0)
	day60Rate = models.FloatField(default=0.0)
	day90Rate = models.FloatField(default=0.0)
	day90Ratem = models.FloatField(default=0.0)
	createDate = models.DateField(default=timezone.now)

	class Meta:
		ordering = ('createDate',)

	unique_together = ('month', 'createDate')

class CollectNum(models.Model):
	newAdd = models.IntegerField(default=0)
	newCollectMl1 = models.IntegerField(default=0)
	newCollectMu1 = models.IntegerField(default=0)
	threeDayCollect = models.IntegerField(default=0)
	threeDayCollectRate = models.FloatField(default=0.0)
	createDate = models.DateField(primary_key=True,default=timezone.now)

	class Meta:
		ordering = ('createDate',)

class CollectDis(models.Model):
	dayto3 = models.IntegerField(default=0)
	dayto10 = models.IntegerField(default=0)
	dayto20 = models.IntegerField(default=0)
	dayto30 = models.IntegerField(default=0)
	dayto60 = models.IntegerField(default=0)
	dayto90 = models.IntegerField(default=0)
	dayover90 = models.IntegerField(default=0)
	currentNum = models.IntegerField(default=0)
	createDate = models.DateField(primary_key=True,default=timezone.now)

	class Meta:
		ordering = ('createDate',)

#market

class MarketNum(models.Model):
	applyPass = models.IntegerField(default=0)
	firstDayT = models.IntegerField(default=0)
	firstDay = models.IntegerField(default=0)
	firstDayRate = models.FloatField(default=0.0)
	tryRate = models.IntegerField(default=0)
	secondDay = models.IntegerField(default=0)
	secondDayRate = models.FloatField(default=0.0)
	thirdDay = models.IntegerField(default=0)
	thirdDayRate = models.FloatField(default=0.0)
	paidNum = models.IntegerField(default=0)
	paidRate = models.FloatField(default=0.0)
	auditTime = models.IntegerField(default=0)
	auditTimeWit = models.IntegerField(default=0)
	auditTimeToday = models.IntegerField(default=0)
	createDate = models.DateField(primary_key=True,default=timezone.now)

	class Meta:
		ordering = ('createDate',)

#aeye

class AeyePassRate(models.Model):
	applyNum = models.IntegerField(default=0)
	passNum = models.IntegerField(default=0)
	passRate = models.FloatField(default=0.0)
	createDate = models.DateField(primary_key=True,default=timezone.now)

	class Meta:
		ordering = ('createDate',)

class AeyeGetRate(models.Model):
	tryNum = models.IntegerField(default=0)
	sucNum = models.IntegerField(default=0)
	sucRate = models.FloatField(default=0.0)
	createDate = models.DateField(primary_key=True,default=timezone.now)

	class Meta:
		ordering = ('createDate',)

class AeyeDelayRate(models.Model):
	delayRate0 = models.FloatField(default=0.0)
	delayRate3 = models.FloatField(default=0.0)
	delayRate7 = models.FloatField(default=0.0)
	delayRate10 = models.FloatField(default=0.0)
	delayRate20 = models.FloatField(default=0.0)
	delayRateM1 = models.FloatField(default=0.0)
	delayRateM2 = models.FloatField(default=0.0)
	delayRateM3 = models.FloatField(default=0.0)
	createDate = models.DateField(primary_key=True,default=timezone.now)

	class Meta:
		ordering = ('createDate',)

class AeyeDelayRateNO(models.Model):
	newDelayRate3 = models.FloatField(default=0.0)
	newRepaySum = models.IntegerField(default=0)
	newPaid = models.IntegerField(default=0)
	oldDelayRate3 = models.FloatField(default=0.0)
	oldRepaySum = models.IntegerField(default=0)
	oldPaid = models.IntegerField(default=0)
	createDate = models.DateField(primary_key=True,default=timezone.now)

	class Meta:
		ordering = ('createDate',)
