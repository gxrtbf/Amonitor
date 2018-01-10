$(document).ready(function(){
    var cdata = {
        'table': "flowpaidmoney",
        'content': "list"
    };
    $.ajax({
        type: 'POST',
        url: "../api/v1/day/?format=json",
        data: {
            para: JSON.stringify(cdata),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
        },
        success: function(dataset){
            console.log(dataset);
            var myChart = echarts.init(document.getElementById('repaymentMoney'));
            var times = [];
            var money = [];
            for(i=0;i<dataset.length;i++)
            {
                times.push(dataset[i]['createDate']);
                money.push(dataset[i]['paidMoney']);
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
                xAxis: [{
                    type: 'category',
                    axisLine: {
                        lineStyle: {
                            color: '#57617B'
                        }
                    },
                    data: times
                }],
                yAxis: [{
                    type: 'value',
                    axisTick: {
                        show: false
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#57617B'
                        }
                    },
                    axisLabel: {
                        margin: 10,
                        textStyle: {
                            fontSize: 14
                        }
                    },
                }],
                series: [{
                    name: '还款金额',
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
        }
    });
});