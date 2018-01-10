from rest_framework import serializers

# #index
from models import IndexHead, IndexDash, IndexHopper, IndexCity, IndexAcrepay

class IndexHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexHead
        fields = ('tradeMoney', 'tradeMoney', 'tradeNum', 'activeUser', 'sumUser', 'createDate')

class IndexDashSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexDash
        fields = ('avgTermNum', 'avgMoney', 'avgServiceMoney', 'createDate')

class IndexHopperSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexHopper
        fields = ('register', 'applys', 'passs', 'loan', 'reloan', 'createDate')

class IndexCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexCity
        fields = ('cityName', 'numInCity', 'createDate')

class IndexAcrepaySerializer(serializers.ModelSerializer):
    class Meta:
        model = IndexAcrepay
        fields = ('allRepayMoney', 'acRepayMoney', 'repayRate', 'createDate')


#userInfo
from models import UserAge, UserAgeAll, UserSex, UserSexAll, UserIncrease, UserRest

class UserAgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAge
        fields = ('age1', 'age2', 'age3', 'age4', 'age5', 'createDate')

class UserAgeAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAgeAll
        fields = ('age1', 'age2', 'age3', 'age4', 'age5', 'createDate')

class UserSexSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSex
        fields = ('male', 'female', 'createDate')

class UserSexAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSexAll
        fields = ('male', 'female', 'createDate')

class UserIncreaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIncrease
        fields = ('register', 'allow', 'newApply', 'oldApply', 'createDate')

class UserRestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRest
        fields = ('registerDate', 'currentDate', 'allPass', 'currentActive', 'currentActiveRate', 'createDate')


#flow
from models import FlowLoanMoney, FlowLoanMoneyNO, FlowLoanMoneySum, FlowDelayRate, FlowDelayRateNO, FlowLoanFund, FlowPaidMoney, FlowC2CFund

class FlowLoanMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowLoanMoney
        fields = ('product', 'money', 'createDate')

class FlowLoanMoneyNOSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowLoanMoneyNO
        fields = ('loanOld', 'loanNew', 'createDate')

class FlowLoanMoneySumSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowLoanMoneySum
        fields = ('product', 'money', 'createDate')

class FlowDelayRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowDelayRate
        fields = ('fundName', 'delayRate0', 'delayRate3', 'delayRate7', 'delayRate10', 'delayRate20', 'delayRateM1', 'delayRateM2', 'delayRateM3', 'createDate')

class FlowDelayRateNOSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowDelayRateNO
        fields = ('fundName', 'newDelayRate3', 'newRepaySum', 'newPaid', 'oldDelayRate3', 'oldRepaySum', 'oldPaid', 'createDate', 'createDate')

class FlowLoanFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowLoanFund
        fields = ('fundName', 'sumMoney', 'createDate')

class FlowPaidMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowPaidMoney
        fields = ('paidMoney', 'createDate')

class FlowC2CFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowC2CFund
        fields = ('member', 'loanCount', 'loanMoney', 'loanCountTerm', 'loanCountTermNo', 'delayRate0', 'allCountTerm', 'delayRate7', 'CountTerm7', 'createDate')

#collect
from models import CollectRate, CollectNum, CollectDis

class CollectRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectRate
        fields = ('month', 'day4Rate', 'day7Rate', 'day15Rate', 'day30Rate', 'day60Rate', 'day90Rate', 'day90Ratem','createDate')

class CollectNumSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectNum
        fields = ('newAdd', 'newCollectMl1', 'newCollectMu1', 'threeDayCollect', 'threeDayCollectRate', 'createDate')

class CollectDisSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectDis
        fields = ('dayto3', 'dayto10', 'dayto20', 'dayto30', 'dayto60', 'dayto90', 'dayover90', 'currentNum','createDate')

#market
from models import MarketNum

class MarketNumSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketNum
        fields = ('applyPass', 'firstDayT', 'firstDay', 'firstDayRate', 'tryRate', 'secondDay', 'secondDayRate', 'thirdDay', 'thirdDayRate', 'paidNum', 'paidRate', 'auditTime', 'auditTimeWit','auditTimeToday','createDate')

#aeye

from models import AeyePassRate, AeyeGetRate, AeyeDelayRate, AeyeDelayRateNO

class AeyePassRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AeyePassRate
        fields = ('applyNum', 'passNum', 'passRate', 'createDate')

class AeyeGetRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AeyeGetRate
        fields = ('tryNum', 'sucNum', 'sucRate', 'createDate')

class AeyeDelayRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AeyeDelayRate
        fields = ('delayRate0', 'delayRate3', 'delayRate7', 'delayRate10', 'delayRate20', 'delayRateM1', 'delayRateM2', 'delayRateM3', 'createDate')

class AeyeDelayRateNOSerializer(serializers.ModelSerializer):
    class Meta:
        model = AeyeDelayRateNO
        fields = ('newDelayRate3', 'newRepaySum', 'newPaid', 'oldDelayRate3', 'oldRepaySum', 'oldPaid', 'createDate', 'createDate')