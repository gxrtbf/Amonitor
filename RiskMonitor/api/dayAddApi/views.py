# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import permission_required


# #index
from models import IndexHead,IndexDash,IndexHopper,IndexCity,IndexAcrepay
from serializers import IndexHeadSerializer,IndexDashSerializer,IndexHopperSerializer,IndexCitySerializer,IndexAcrepaySerializer

#userInfo
from models import UserAge,UserAgeAll,UserSex,UserSexAll,UserIncrease
from serializers import UserAgeSerializer,UserAgeAllSerializer,UserSexSerializer,UserSexAllSerializer,UserIncreaseSerializer

#flow
from models import FlowLoanMoney,FlowLoanMoneyNO,FlowLoanMoneySum,FlowDelayRate,FlowDelayRateNO
from serializers import FlowLoanMoneySerializer,FlowLoanMoneyNOSerializer,FlowLoanMoneySumSerializer,FlowDelayRateSerializer,FlowDelayRateNOSerializer

#collect
from models import CollectRate,CollectNum,CollectDis
from serializers import CollectRateSerializer,CollectNumSerializer,CollectDisSerializer

#market
from models import MarketNum
from serializers import MarketNumSerializer

#aeya
from models import AeyePassRate,AeyeGetRate,AeyeDelayRate,AeyeDelayRateNO
from serializers import AeyePassRateSerializer,AeyeGetRateSerializer,AeyeDelayRateSerializer,AeyeDelayRateNOSerializer

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

#@permission_required('part_admin.financePage')
@api_view(['GET'])
def indexhead_item(request):
    if request.method == 'GET':
    	tables = request.GET.get('table',None)
    	if tables:
    		objectModel = tableModel[tables]['models']
    		objectSerializer = tableModel[tables]['serializers']

    		fundName = request.GET.get('fundName',None)
    		if fundName:
    			temp = objectModel.objects.filter(fundName=fundName)
    			serializer = objectSerializer(temp, many=True)
    			return Response(serializer.data)

    		content = request.GET.get('content',None)
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