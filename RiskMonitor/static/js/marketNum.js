$(document).ready(function(){
    $.get("../api/v1/day?format=json&table=marketnum&content=list",function(dataset){
        console.log(dataset);

        var applyPass = [];
        var firstDayT = [];
        var firstDay = [];
        var firstDayRate = [];
        var tryRate = [];
        var auditTime = [];
        var auditTimeWit = [];
        var auditTimeToday = [];

        var paidNum = [];
        var paidRate = [];

        var defalutRate = [];

        var times = [];

        for(i=0;i<dataset.length;i++)
        {
            applyPass.push(dataset[i]['applyPass']);
            firstDayT.push(dataset[i]['firstDayT']);
            firstDay.push(dataset[i]['firstDay']);
            firstDayRate.push(dataset[i]['firstDayRate']);
            tryRate.push(dataset[i]['tryRate']);
            auditTime.push(dataset[i]['auditTime']);
            auditTimeWit.push(dataset[i]['auditTimeWit']);
            auditTimeToday.push(dataset[i]['auditTimeToday']);

            paidNum.push(dataset[i]['paidNum']);
            paidRate.push(dataset[i]['paidRate']);

            times.push(dataset[i]['createDate'])

            defalutRate.push(Math.round(100-dataset[i]['firstDay']/dataset[i]['firstDayT']*100))
        }

        var myChart = echarts.init(document.getElementById('main'));
        var option = {
            title: {
                text: '当日贷款情况',
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
                data: ['通过量','当日尝试提现数','当日尝试提现率','当日提现成功数','当日提现成功率'],
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
                boundaryGap: false,
                axisLine: {
                    lineStyle: {
                        color: '#57617B'
                    }
                },
                data: times
            }],
            yAxis: [{
                type: 'value',
                name: '人数',
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
            },
            {
                    type: 'value',
                    name: '%',
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
            series: [
                {
                    name:'通过量',
                    type:'bar',
                    data:applyPass,
                    itemStyle:{  
                        normal:{color:'#f0ad4e'}  
                    } 
                },
                {
                    name:'当日尝试提现数',
                    type:'bar',
                    data:firstDayT,
                    itemStyle:{  
                        normal:{color:'green'}  
                    } 
                },
                {
                    name:'当日提现成功数',
                    type:'bar',
                    data:firstDay,
                    itemStyle:{  
                        normal:{color:'red'}  
                    } 
                },
                {
                    name:'当日尝试提现率',
                    type:'line',
                    yAxisIndex: 1,
                    data:tryRate,
                    itemStyle:{  
                        normal:{color:'#5cb85c'}  
                    } 
                },
                {
                    name:'当日提现成功率',
                    type:'line',
                    yAxisIndex: 1,
                    data:firstDayRate,
                    itemStyle:{  
                        normal:{color:'#0f88eb'}  
                    } 
                }
            ]
        };
        myChart.setOption(option);

        var myChart = echarts.init(document.getElementById('main2'));
        var option = {
            title: {
                text: '当日贷款曲线与审核时间的关系',
                textStyle: {
                    fontWeight: 'normal',
                    fontSize: 20,
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
                data: ['当日尝试提现率','当日提现失败率','当日申请审核时间'],
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
                boundaryGap: false,
                axisLine: {
                    lineStyle: {
                        color: '#57617B'
                    }
                },
                data: times
            }],
            yAxis: [{
                type: 'value',
                name: '分钟',
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
            },
            {
                    type: 'value',
                    name: '%',
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
            series: [
                {
                    name:'当日尝试提现率',
                    type:'line',
                    yAxisIndex: 1,
                    data:tryRate,
                    itemStyle:{  
                        normal:{color:'#F59701'}  
                    } 
                },
                {
                    name:'当日提现失败率',
                    type:'line',
                    yAxisIndex: 1,
                    data:defalutRate,
                    itemStyle:{  
                        normal:{color:'#0f88eb'}  
                    } 
                },
                {
                    name:'当日申请审核时间',
                    type:'bar',
                    data:auditTimeToday,
                    itemStyle:{  
                        normal:{color:'#5cb85c'}  
                    } 
                }


            ]
        };
        myChart.setOption(option);

        html_result = '' + 
        '<table class="table" style="width: 100%;margin:0 auto;"> '+
            '<thead class="fixedThead" style="width: 100%"> '+
                '<tr style="margin:0 auto;"><th>时间</th><th>当日通过申请数</th><th>当日尝试提现数</th><th>当日成功提现数</th><th>至今成功提现数</th>' +
                '<th>当日尝试提现率</th><th>当日成功提现率</th><th>至今成功提现率</th>'+
                '<th>审核时间（总）</th><th>当日申请审核时间</th></tr>'+
            '</thead> '+
        '<tbody class="scrollTbody" style="width: 100%;"> '
        lnum = times.length
        for (var i = 1; i <= lnum; i++)
        {
            html_result += '<tr>';
            html_result += '<td>'+times[lnum-i]+'</td>';
            html_result += '<td>'+applyPass[lnum-i]+'</td>';
            html_result += '<td>'+firstDayT[lnum-i]+'</td>';
            html_result += '<td>'+firstDay[lnum-i]+'</td>';
            // html_result += '<td>'+secondDay[lnum-i]+'</td>';
            // html_result += '<td>'+thirdDay[lnum-i]+'</td>';
            html_result += '<td>'+paidNum[lnum-i]+'</td>';
            html_result += '<td>'+tryRate[lnum-i]+"%"+'</td>';
            html_result += '<td>'+firstDayRate[lnum-i]+"%"+'</td>';
            // html_result += '<td>'+secondDayRate[lnum-i]+"%"+'</td>';
            // html_result += '<td>'+thirdDayRate[lnum-i]+"%"+'</td>';
            html_result += '<td>'+paidRate[lnum-i]+"%"+'</td>';
            html_result += '<td>'+auditTime[lnum-i]+"min"+'</td>';
            // html_result += '<td>'+auditTimeWit[lnum-i]+"min"+'</td>';
            html_result += '<td>'+auditTimeToday[lnum-i]+"min"+'</td>';
            html_result += '</tr>';
        }
        html_result += '</tbody> </table> '
        document.getElementById('data').innerHTML=html_result;
    });
});