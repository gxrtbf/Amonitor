# -*- coding: utf-8 -*-
import datetime
import numpy
#日志地址
log_path = 'update.log'

#修正格式
def set_default(obj):
	if isinstance(obj, datetime.datetime):
		return obj.strftime('%Y-%m-%d %H:%M:%S')
	elif isinstance(obj, int):
		return round(float(obj),2)
	elif isinstance(obj, numpy.int64):
		return round(float(obj),2)
	elif isinstance(obj, float):
		return round(float(obj),2)
	elif isinstance(obj, object):
		return str(obj)
	else:
		return str(obj)
		raise TypeError('%r is not JSON serializable' % obj)

#sex
sex_label = {
	'1':'男',
	'2':'女'
}

#age
age_label = {
	'point':[-1,18,25,33,41,100],
	'label':['18岁及以下','19-25岁','26-33岁','34-41岁','42岁及以上']
}

#local
local_label = {
	'55566':u'四川',
	'45463':u'广东',
	'45465':u'湖北',
	'45464':u'湖南',
	'45462':u'广西',
	'35362':u'福建',
	'35365':u'江苏',
	'35363':u'安徽',
	'45466':u'河南',
	'35361':u'江西',
	'35360':u'山东',
	'35364':u'浙江',
	'15164':u'河北',
	'15163':u'山西',
	'55567':u'重庆',
	'25266':u'辽宁',
	'55564':u'云南',
	'55565':u'贵州',
	'65666':u'陕西',
	'25264':u'黑龙江',
	'25265':u'吉林',
	'15162':u'内蒙古',
	'65665':u'甘肃',
	'45461':u'海南',
	'35366':u'上海',
	'65662':u'新疆',
	'65663':u'宁夏',
	'15165':u'天津',
	'15166':u'北京',
	'65664':u'青海',
	'55563':u'西藏'
}

#loan_num
loan_label = {
	'point':[-1,1,2,4,7,100],
	'label':['1次','2次','3-4次','5-7次','8次以上']
}

#product
product = {
    '1':u'及时雨',
    '2':u'闪电贷',
    '3':u'商品贷',
    '4':u'现金分期',
    '5':u'闪小贷',
    '101':u'魔贷',
    '102':u'五斗米',
    '103':u'仟元贷',
    '104':u'爱多贷',
    # '105':u'王者钱贷',
    '107':u'拿点花',
    '108':u'付呗零用钱',
    '109':u'有钱来了',
    '111':u'速融超',
    '112':u'钱好借',
    '113':u'马上有钱',
    '114':u'借袋钱',
    '115':u'点点花',
}


#逾期率
delayRate = {
    'label':['首逾率','逾期率3+','逾期率7+','逾期率10+','逾期率20+','逾期率M1','逾期率M2','逾期率M3'],
    'trend':{
        'times':['2017-09-19'],
        '首逾率':0,
        '逾期率3+':0,
        '逾期率7+':0,
        '逾期率10+':0,
        '逾期率20+':0,
        '逾期率M1':0,
        '逾期率M2':0,
        '逾期率M3':0
    }
}

#催收人员
collectMember = {
	'M1':{
		'self': {
			'2017041018074105e80eed8f884b97a1c550a148548c80':'朱启阳(geoff)',
			'201705121519023e53977fd48f43a1a1d267da76bc2400':'董学浩(Wade)',
			'201704121314437cc90d73101240438eeb7826f6937700':'王聿松(Lison)',
			'20170803145229cfc305df5fe647eea281ec7fc538119c':'李金龙(Kevin)',
			'2017080314544787e2b651e0f341ad8b7a409dc68ee24d':'李静萍(Morgana)',
			'20170803145300378be2322ca24848948b93847673e7a5':'胡军(Zed)',
			'20170523153116e295a60d5df2405c94e91363b91358ac':'何谦(Alisa)',
			'20170901100439af50120e72f145fcb8c776fe14581336':'郑伟(Colin)',
			'20170901100510e79414cfb09a45499a81019ad4159dec':'施弘祥(Aaron)',
			'20170901100553a3689b61a6fb47f3b1a7c2a34d52efbb':'庹正寰(Wilson)',
			'20170901100348c0bf4de584d14b028cc33e419e716ac3':'郭锐(Rick)',
			'201709070924396645c21d7b144f11ab60d8673c5672cc':'阎苗苗(Nemo)',
			'20170907093103e8e663499a3a49b0aed363bfc9ba3e73':'王振国(Apple)',
			'20171005092012837194f3a00245b3ba4c30658c68a4e0':'胡红(Ruby)',
			'20171005092151e5d2ef5b7927419182cbe211accfe144':'齐峰(Asa)',
			'201710050922271a6cebe806a149d68daa6a2a7084b923':'石鹏飞(Bing)'
		},
		'changxin': {
			'2017041213111369c58a9ac1e54c02908008462c0e15d8':'昌信01(changxin01)',
			'201704121312417673248b382c4c3ead357d57e89c804d':'昌信02(changxin02)',
			'201704121313001c752fce2bd94c0496fbd22791ec9c5f':'昌信03(changxin03)',
			'201704121313268898c8a4ce7c4819a80ad6defd7164b9':'昌信04(changxin04)',
			'2017041720014778ec6f83bd894f818f01b07b7629b313':'昌信05(changxin05)',
			'2017041720023461ecf7effddf43b2b83676b9df5b8a49':'昌信06(changxin06)',
			'20170429110239f727d36ac11946e897d65a3cefa141f1':'昌信07(changxin07)',
			'20170531202949424d301638644fa1bbbfb1821c7e9ed4':'昌信08(changxin08)',
			'20170531203022fe15181ee94244d7801d42ee2cb251f7':'昌信09(changxin09)',
			'201705312030594efbffe8cf3b44dda07a1baefcdc52f3':'昌信10(changxin10)',
		},
		'pancheng': {
			'20170901101507106f08a45dc94c1795c8f1fabb09b7cd':'磐辰01(pancheng01)',
			'2017090110152347be1c3daec947c987f929b1161d0317':'磐辰02(pancheng02)',
			'201709011015571271f59e02b7475abe04092b072c0842':'磐辰03(pancheng03)',
			'201709011016128055b6c73dca4a63a47356591c808533':'磐辰04(pancheng04)',
			'20170901101628e2bc0fb3e54641e086b7c9487519efc3':'磐辰05(pancheng05)',
			'2017090110165043679a0b36e74600874b867c7e5cfc3c':'磐辰06(pancheng06)',
			'20170907085950f7d634157f0b44a39f2c602d7b3328a6':'磐辰07(pancheng07)',
			'20170907090026e937b37b73c14bb38a11ce0ae57fd708':'磐辰08(pancheng08)',
			'20170907090050c42b27e0bbd6424f8a5e639778875904':'磐辰09(pancheng09)',
			'201709070901102fa4a776e38d4231aaf7c3445ef3b5ee':'磐辰10(pancheng10)',
		},
		'yunchi': {
			'201708171002468c027414059746c68d2e2238fe7d02b9':'云驰11(yunchi11)',
			'2017081710030328c79c7045274273b2ef48a9f5d75ecb':'云驰12(yunchi12)',
			'20170817100325cbcc8acc810942c48174f0d7ff61cd81':'云驰13(yunchi13)',
			'20170817100344bb6145e6348046c09780e1a1ac616821':'云驰14(yunchi14)',
			'201708171004023848b2ac1cd1492ab160bc5bd43eff4c':'云驰15(yunchi15)',
			'20170817100422d8254350a2b44de5b7c1e80c52360859':'云驰16(yunchi16)',
			'2017090709090197226378b7cf4d75b7a38eb9bd035a23':'云驰21(yunchi21)',
			'201709070909206f5010620ff4494ea7aec0b5f9d9278f':'云驰22(yunchi22)',
			'20170907090943371b396332af412b93d36c4135f5edb9':'云驰23(yunchi23)',
			'20170907091009168e3837c5c141daa2a82f1233360512':'云驰24(yunchi24)',
		},
	},
	'M2':{
		'yunchi':{
			'201704121146481799db69609e4cebb3982c00a3deadb2':'云驰01(yunchi01)',
			'20170412115459e080f05aeb084bc3958345f6832108dc':'云驰02(yunchi02)',
			'20170412115900c23a4d6ddd404684bbb0399e2dde4857':'云驰03(yunchi03)',
			'2017041213071471ddbcd91b3d4bf28dd5a0a4e00e7d6f':'云驰04(yunchi04)',
			'20170531203227f94fd74d0c734cd1a5ea2a57a9965f37':'云驰05(yunchi05)',
			'20170531203259cd59c4f96c8e49a0baf92761e3ed1fda':'云驰06(yunchi06)',
			'201705312033328c5eb9e0f9e74b64a7e4de5a5a4e73d9':'云驰07(yunchi07)',
			'20170607182813c5b29facefad499f8222396887f78325':'云驰08(yunchi08)',
			'201706071828497c758785f3a04fc5859e88ae7bf9db93':'云驰09(yunchi09)',
			'20170607182912e00fb4b443774f6bbad73d55e60928e1':'云驰10(yunchi10)',
			'20170901105504fd30fcfa105f4f28ae243f03218ab08c':'云驰17(yunchi17)',
			'201709011055202449f5154bb74e4db992c984630b34f5':'云驰18(yunchi18)',
			'20170901105543728941f485e5429b8941218b4b7c7f15':'云驰19(yunchi19)',
		},
	}
}

#资金方id
fundloanId = {
	u'快乐达连连账户':["'10001'"],
	u'纵横新创':["'10002','10004'"],
	u'口袋理财':["'10003'"],
	u'柚子理财':["'10005'"],
	u'魔贷金融':["'10006','10010','10017'"],
	u'小袋理财':["'10007'"],
	u'爱多贷':["'10008'"],
	# u'暴雷科技':["'10009'"],
	u'拿点花':["'10011'"],
	u'付呗零用钱':["'10012'"],
	u'星火钱包':["'20002','20001'"],
	u'钱好借':["'10016'"],
	u'速融超':["'10015'"],
	# u'小桥钱包':["'10014'"],
	u'马上有钱':["'10018'"],
	u'有钱来了':["'10013'"],
	u'借袋钱':["'10019'"],
	u'点点花':["'10020'"],
}

#c2c_menber

c2c_member = {
	u'terry':["'1028'"],
	u'gaffey':["'1029'"],
	u'yujiahui':["'1030'"],
	u'emily':["'1033'"],
	u'ailsa':["'1036'"],
	u'yulanda':["'1037'"],
	u'haoshiduo':["'1040'"],
	u'zhonglishi':["'1041'"]
	u'vicky':["'1044'"]
}













