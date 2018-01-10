# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import permission_required


# #index
from models import IndexHead, IndexDash, IndexHopper, IndexCity, IndexAcrepay
from serializers import IndexHeadSerializer, IndexDashSerializer, IndexHopperSerializer, IndexCitySerializer, IndexAcrepaySerializer

#userInfo
from models import UserAge, UserAgeAll, UserSex, UserSexAll, UserIncrease, UserRest
from serializers import UserAgeSerializer, UserAgeAllSerializer, UserSexSerializer, UserSexAllSerializer, UserIncreaseSerializer, UserRestSerializer

#flow
from models import FlowLoanMoney, FlowLoanMoneyNO, FlowLoanMoneySum, FlowDelayRate, FlowDelayRateNO, FlowLoanFund, FlowPaidMoney, FlowC2CFund
from serializers import FlowLoanMoneySerializer, FlowLoanMoneyNOSerializer, FlowLoanMoneySumSerializer, FlowDelayRateSerializer, FlowDelayRateNOSerializer, FlowLoanFundSerializer, FlowPaidMoneySerializer, FlowC2CFundSerializer

#collect
from models import CollectRate, CollectNum, CollectDis
from serializers import CollectRateSerializer, CollectNumSerializer, CollectDisSerializer

#market
from models import MarketNum
from serializers import MarketNumSerializer

#aeya
from models import AeyePassRate, AeyeGetRate, AeyeDelayRate, AeyeDelayRateNO
from serializers import AeyePassRateSerializer, AeyeGetRateSerializer, AeyeDelayRateSerializer, AeyeDelayRateNOSerializer

#model dict
tableModel = {
	'indexhead': {
			'models': IndexHead,
			'serializers': IndexHeadSerializer,
	},
	'indexdash': {
			'models': IndexDash,
			'serializers': IndexDashSerializer,
	},
	'indexhopper': {
			'models': IndexHopper,
			'serializers': IndexHopperSerializer,
	},
	'indexcity': {
			'models': IndexCity,
			'serializers': IndexCitySerializer,
	},
	'indexacrepay': {
			'models': IndexAcrepay,
			'serializers': IndexAcrepaySerializer,
	},
	'userage': {
			'models': UserAge,
			'serializers': UserAgeSerializer,
	},
	'userageall': {
			'models': UserAgeAll,
			'serializers': UserAgeAllSerializer,
	},
	'usersex': {
			'models': UserSex,
			'serializers': UserSexSerializer,
	},
	'usersexall': {
			'models': UserSexAll,
			'serializers': UserSexAllSerializer,
	},
	'userincrease': {
			'models': UserIncrease,
			'serializers': UserIncreaseSerializer,
	},
	'userrest': {
			'models': UserRest,
			'serializers': UserRestSerializer,
	},
	'flowloanmoney': {
			'models': FlowLoanMoney,
			'serializers': FlowLoanMoneySerializer,
	},
	'flowloanmoneyno': {
			'models': FlowLoanMoneyNO,
			'serializers': FlowLoanMoneyNOSerializer,
	},
	'flowloanmoneysum': {
			'models': FlowLoanMoneySum,
			'serializers': FlowLoanMoneySumSerializer,
	},
	'flowdelayrate': {
			'models': FlowDelayRate,
			'serializers': FlowDelayRateSerializer,
	},
	'flowdelayrateno': {
			'models': FlowDelayRateNO,
			'serializers': FlowDelayRateNOSerializer,
	},
	'flowloanfund': {
			'models': FlowLoanFund,
			'serializers': FlowLoanFundSerializer,
	},
	'flowpaidmoney': {
			'models': FlowPaidMoney,
			'serializers': FlowPaidMoneySerializer,
	},
	'flowc2c': {
			'models': FlowC2CFund,
			'serializers': FlowC2CFundSerializer,
	},
	'collectrate': {
			'models': CollectRate,
			'serializers': CollectRateSerializer,
	},
	'collectnum': {
			'models': CollectNum,
			'serializers': CollectNumSerializer,
	},
	'collectdis': {
			'models': CollectDis,
			'serializers': CollectDisSerializer,
	},
	'marketnum': {
			'models': MarketNum,
			'serializers': MarketNumSerializer,
	},
	'aeyepassrate': {
			'models': AeyePassRate,
			'serializers': AeyePassRateSerializer,
	},
	'aeyegetrate': {
			'models': AeyeGetRate,
			'serializers': AeyeGetRateSerializer,
	},
	'aeyedelayrate': {
			'models': AeyeDelayRate,
			'serializers': AeyeDelayRateSerializer,
	},
	'aeyedelayrateno': {
			'models': AeyeDelayRateNO,
			'serializers': AeyeDelayRateNOSerializer,
	},
}

import datetime
from django.db.models import Max

#@permission_required('part_admin.dayapi')
@api_view(['POST'])
def indexhead_item(request):
    if request.method == 'POST':

    	paralist = eval(request.POST.get('para',None))
    	tables = paralist.get('table',None)
    	content = paralist.get('content',None)
    	
    	if tables and content:

    		objectModel = tableModel[tables]['models']
    		objectSerializer = tableModel[tables]['serializers']

    		para = paralist.get('para',[])
    		print para
    		if para:
    			temp = objectModel.objects.all()
    			filterstrtemp = "temp.filter({}{}='{}')"
    			for xkey in para:
    				key = xkey.get('key','')
    				value = xkey.get('value','')
    				way = xkey.get('way','')
    				way = '__' + way if way else ''
    				filterstr = filterstrtemp.format(key,way,value)
    				temp = eval(filterstr)
    			serializer = objectSerializer(temp, many=True)

    			return Response(serializer.data)
    		else:
    			if content == 'item':
	    			#yesterday = str(datetime.datetime.now() - datetime.timedelta(days=1))[:10]
	    			yesterday = str(objectModel.objects.all().aggregate(Max('createDate')).values()[0])[:10]
	    			temp = objectModel.objects.filter(createDate=yesterday)
	    			serializer = objectSerializer(temp, many=True)
	    			return Response(serializer.data)
	    		elif content == 'list':
	    			temp = objectModel.objects.all()
	    			serializer = objectSerializer(temp, many=True)
	    			return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)