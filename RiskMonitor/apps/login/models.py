# -*- coding: utf-8 -*-

from django.db import models

class User(models.Model):
	
	email = models.EmailField('邮箱',max_length=20,primary_key=True)
	username = models.CharField('姓名',max_length=20)
	password = models.CharField('密码',max_length=20)
	level = models.IntegerField('等级')

	def __unicode__(self):
		return self.username
