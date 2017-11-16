$(document).ready(function(){
    $.get("../api/index?format=json&table=flowloanmoneyno&content=list",function(dataset){
        var myChart = echarts.init(document.getElementById('loanNO'));
        var loanNew = [];
        var loanOld = [];
        var times = [];
        for(i=0;i<dataset.length;i++)
        {
            loanNew.push(dataset[i]['loanNew']);
            loanOld.push(dataset[i]['loanOld']);
            times.push(dataset[i]['createDate']);
        }
        var option = {
            title: {
                text: '每日贷款情况(金额)'
            },
            tooltip : {
                trigger: 'axis',
                axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                    type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                }
            },
            legend: {
                data:['老客贷款金额','新客贷款金额']
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis : [
                {
                    type : 'category',
                    data : times
                }
            ],
            yAxis : [
                {
                    type : 'value'
                }
            ],
            dataZoom: [
                {
                    type: 'inside',
                    start: 80,
                    end: 100
                },
                {
                    start: 0,
                    end: 10,
                    handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                    handleSize: '80%',
                    handleStyle: {
                        color: '#fff',
                        shadowBlur: 3,
                        shadowColor: 'rgba(0, 0, 0, 0.6)',
                        shadowOffsetX: 2,
                        shadowOffsetY: 2
                    }
                }
            ],
            series : [
                {
                    name:'老客贷款金额',
                    type:'bar',
                    stack: '贷款金额',
                    itemStyle:{
                        normal:{
                            color:'#337ab7',
                        },
                    },
                    data:loanOld
                },
                {
                    name:'新客贷款金额',
                    type:'bar',
                    stack: '贷款金额',
                    itemStyle:{
                        normal:{
                            color:'#5cb85c',
                        },
                    },
                    data:loanNew
                }
            ]
        };
        myChart.setOption(option);
    });
    $.get("../api/index?format=json&table=flowloanmoneysum&content=item",function(dataset){
        var product = [];
        var money = [];
        for(i=0;i<dataset.length;i++)
        {
            product.push(dataset[i]['product']);
            money.push(dataset[i]['money']);
        }
        var myChart = echarts.init(document.getElementById('sumLoanMoney'));
        var option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                },
                formatter: "{a} <br/>{b} : {c}"
            },
            grid: {
                left: '9%',
                right: '8%',
                bottom: '5%',
                top:'2%',
                containLabel: true
            },
            xAxis: {
                type: 'value',
                name:'金额',
                nameLocation:'end',
                position:'top',
                axisTick: {
                     show: false
                },
                axisLabel: {
                    formatter: '{value}',
                }
            },
            yAxis: {
                type: 'category',
                name:'产品名称',
                nameLocation:'start',
                axisTick: {
                    show: false
                },
                inverse:'true',
                data: product
            },
            series: [{
                name: '贷款金额',
                type: 'bar',
                itemStyle: {
                    normal: {
                        color: '#26C0C0'
                    }
                },
            data: money
            }]
        };
        myChart.setOption(option);
    });
    $.get("../api/index?format=json&table=flowloanmoney&content=item",function(dataset){
        var myChart = echarts.init(document.getElementById('sumLoanMoneyT'));
        var product = [];
        var money = [];
        for(i=0;i<dataset.length;i++)
        {
            if(dataset[i]['product']!='All'){
                product.push(dataset[i]['product']);
                money.push(dataset[i]['money']);
            }
        }
        var option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                },
                formatter: "{a} <br/>{b} : {c}"
            },
            grid: {
                left: '9%',
                right: '8%',
                bottom: '5%',
                top:'2%',
                containLabel: true
            },
            xAxis: {
                type: 'value',
                name:'金额',
                nameLocation:'end',
                position:'top',
                axisTick: {
                     show: false
                },
                axisLabel: {
                    formatter: '{value}',
                }
            },
            yAxis: {
                type: 'category',
                name:'产品名称',
                nameLocation:'start',
                axisTick: {
                    show: false
                },
                inverse:'true',
                data: product
            },
            series: [{
                name: '贷款金额',
                type: 'bar',
                itemStyle: {
                    normal: {
                        color: '#26C0C0'
                    }
                },
            data: money
            }]
        };
        myChart.setOption(option);
    });
});