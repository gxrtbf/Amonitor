# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import permission_required


#添加路径
# sys.path.insert(0,os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from actualCal.finance import finance

#@permission_required('part_admin.financePage')
@api_view(['GET'])
def actime_item(request):
	if request.method == 'GET':
		tables = request.GET.get('table',None)
		if tables == 'finance':
			content = request.GET.get('content',None)
			if content == 'list':
				todayLoan_dict = {'todayLoan':{}}
				todayLoan_dict['todayLoan'] = finance.todayLoan()
				return Response(todayLoan_dict)
			elif content == 'item':
				loanDetail = {'hours':[],'cumMoney':[]}
				loanDetail = finance.todayLoanDetail()
				return Response(loanDetail)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
