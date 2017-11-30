$(document).ready(function(){
    $.get("../api/v1/actime/?format=json&table=finance&content=list",function(dataset){
        console.log(dataset);
        document.getElementById("header1").innerHTML = '今日已贷总金额：' + dataset.todayLoan["paidAll"] + ' ¥ ';
        html_result = ''
        for(var i in dataset.todayLoan.fundId) 
        {
            html_result += '<div style="display: inline-block;background-color: #5cb85c;color: #fff;width: 15%;text-align:center;border:3px solid #f0ad4e;margin: 5px">'
            html_result += '<h3>'
            html_result += i
            html_result += '</h3>'
            html_result += '<h4>'
            html_result += dataset.todayLoan.fundId[i]
            html_result += '</h4>'
            html_result += '</div>'
        } 
        document.getElementById('content').innerHTML=html_result;

    });
    $.get("../api/v1/actime/?format=json&table=finance&content=item",function(dataset){
        var myChart = echarts.init(document.getElementById('main'));
        var option = {
            title: {
                text: '累计贷款曲线',
                textStyle: {
                    fontWeight: 'normal',
                    fontSize: 25,
                },
                left: '6%'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    lineStyle: {
                        color: '#57617B'
                    }
                }
            },
            legend: {
                icon: 'rect',
                itemWidth: 14,
                itemHeight: 5,
                itemGap: 13,
                data: ['累计贷款量'],
                right: '4%',
                textStyle: {
                    fontSize: 12,
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: [{
                type: 'category',
                axisLine: {
                    lineStyle: {
                        color: '#57617B'
                    }
                },
                data: dataset['hours']
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
                splitLine: {
                    show:false
                }
            }],
            series: [
            {
                name: '累计贷款量',
                type: 'bar',
                smooth: true,
                data: dataset['cumMoney'],
                itemStyle:{  
                    normal:{color:'#f0ad4e'}  
                } 
            }]
        };
        myChart.setOption(option);

        var myChart = echarts.init(document.getElementById('main1'));
        var option = {
            title: {
                text: '今日贷款',
                textStyle: {
                    fontWeight: 'normal',
                    fontSize: 25,
                },
                left: '6%'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    lineStyle: {
                        color: '#57617B'
                    }
                }
            },
            legend: {
                icon: 'rect',
                itemWidth: 14,
                itemHeight: 5,
                itemGap: 13,
                data: ['今日分时贷款量'],
                right: '4%',
                textStyle: {
                    fontSize: 12,
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: [{
                type: 'category',
                axisPointer: {
                    type: 'shadow'
                },
                data: dataset['hours']
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
                splitLine: {
                    show:false
                }
            }],
            series: [
            {
                name: '今日分时贷款量',
                type: 'bar',
                smooth: true,
                data: dataset['money'],
                itemStyle:{  
                    normal:{color:'#f0ad4e'}  
                } 
            }]
        };
        myChart.setOption(option);
    });
 });




