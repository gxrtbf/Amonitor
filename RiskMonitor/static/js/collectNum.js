$(document).ready(function(){
    var cdata = {
        'table': "collectdis",
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

            var currentNum = [];
            var currentNumDis1 = [];
            var currentNumDis2 = [];
            var currentNumDis3 = [];
            var currentNumDis4 = [];
            var currentNumDis5 = [];
            var currentNumDis6 = [];

            var currentNumM10 = [];
            var currentNumM11 = [];

            var times = [];

            for(i=0;i<dataset.length;i++)
            {
                currentNum.push(dataset[i]['currentNum'] -dataset[i]['dayover90']);
                currentNumDis1.push(dataset[i]['dayto3']);
                currentNumDis2.push(dataset[i]['dayto10']);
                currentNumDis3.push(dataset[i]['dayto20']);
                currentNumDis4.push(dataset[i]['dayto30']);
                currentNumDis5.push(dataset[i]['dayto60']);
                currentNumDis6.push(dataset[i]['dayto90']);

                currentNumM10.push(
                    dataset[i]['dayto3'] + dataset[i]['dayto7'] + dataset[i]['dayto10'] + dataset[i]['dayto20'] + dataset[i]['dayto30']
                );
                currentNumM11.push(
                    dataset[i]['dayto60'] + dataset[i]['dayto90']
                );
                times.push(dataset[i]['createDate']);
            }
            var myChart = echarts.init(document.getElementById('main'));
            var option = {
                title: {
                    text: '逾期90天内待催回案件数',
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
                    data: ['当前待催回案件数'],
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
                yAxis: [
                    {
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
                    },
                    {
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
                dataZoom: [
                    {
                        type: 'inside',
                        start: 80,
                        end: 150
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
                        name: '当前待催回案件数',
                        type: 'bar',
                        smooth: true,
                        data: currentNum,
                        itemStyle:{  
                            normal:{color:'#008A83'}  
                        } 
                    },
                ]
            };
            myChart.setOption(option);
            var myChart = echarts.init(document.getElementById('main2'));
            var option = {
                title: {
                    text: '当前案件逾期天数分布情况',
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
                    data: ['1-3天','4-10天','11-20天','21-30天','31-60天','61-90天'],
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
                yAxis: [
                    {
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
                    },
                    {
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
                dataZoom: [
                    {
                        type: 'inside',
                        start: 80,
                        end: 150
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
                        name:'1-3天',
                        type:'line',
                        yAxisIndex: 1,
                        data:currentNumDis1,
                        itemStyle:{  
                            normal:{color:'#FF7438'}  
                        } 
                    },
                    {
                        name:'4-10天',
                        type:'line',
                        yAxisIndex: 1,
                        data:currentNumDis2,
                        itemStyle:{  
                            normal:{color:'#F79383'}  
                        } 
                    },
                    {
                        name:'11-20天',
                        type:'line',
                        yAxisIndex: 1,
                        data:currentNumDis3,
                        itemStyle:{  
                            normal:{color:'#ABF637'}  
                        } 
                    },
                    {
                        name:'21-30天',
                        type:'line',
                        yAxisIndex: 1,
                        data:currentNumDis4,
                        itemStyle:{  
                            normal:{color:'#24B455'}  
                        } 
                    },
                    {
                        name:'31-60天',
                        type:'line',
                        yAxisIndex: 1,
                        data:currentNumDis5,
                        itemStyle:{  
                            normal:{color:'#008A83'}  
                        } 
                    },
                    {
                        name:'61-90天',
                        type:'line',
                        yAxisIndex: 1,
                        data:currentNumDis6,
                        itemStyle:{  
                            normal:{color:'#022D33'}  
                        } 
                    },
                ]
            };
            myChart.setOption(option);
        }
    });
    var cdata = {
        'table': "collectdis",
        'content': "item"
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
            var myChart = echarts.init(document.getElementById('collectDis'));
            option = {
                title : {
                    text: '昨日案件逾期天数分布情况',
                    x:'center'
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{b} : {c} ({d}%)"
                },
                legend: {
                    x : 'center',
                    y : 'bottom',
                    data : ['1-3天','4-10天','11-20天','21-30天','31-60天','61-90天']
                },
                toolbox: {
                    show : true,
                    feature : {
                        mark : {show: true},
                        dataView : {show: true, readOnly: false},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                series : [
                    {
                        name:'面积模式',
                        type:'pie',
                        radius : [40, 150],
                        center : ['50%', '50%'],
                        data:[
                            {value:dataset[0]['dayto3'], name:'1-3天'},
                            {value:dataset[0]['dayto10'], name:'4-10天'},
                            {value:dataset[0]['dayto20'], name:'11-20天'},
                            {value:dataset[0]['dayto30'], name:'21-30天'},
                            {value:dataset[0]['dayto60'], name:'31-60天'},
                            {value:dataset[0]['dayto90'], name:'61-90天'},
                        ]
                    }
                ]
            };
            myChart.setOption(option);

        var cdata = {
            'table': "collectnum",
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

                console.log(dataset)
                var yesterdayNew = [];
                var yesterdayPaid300 = [];
                var yesterdayPaid301 = [];
                var threeDayPaid = [];
                var NewPaidRate = [];
                var times = [];
                for(i=0;i<dataset.length;i++)
                {
                    yesterdayNew.push(dataset[i]['newAdd']);
                    yesterdayPaid300.push(dataset[i]['newCollectMu1']);
                    yesterdayPaid301.push(dataset[i]['newCollectMl1']);
                    threeDayPaid.push(dataset[i]['threeDayCollect']);
                    NewPaidRate.push(dataset[i]['threeDayCollectRate']);

                    times.push(dataset[i]['createDate']);
                }

                var myChart = echarts.init(document.getElementById('main1'));
                var option = {
                    title: {
                        text: '催回案件数',
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
                        data: ['当日新增案件数','当日催回案件数M1-','当日催回案件数M1+','三日催回案件数','三日催回案件率'],
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
                    yAxis: [
                        {
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
                        },
                        {
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
                            name: '当日新增案件数',
                            type: 'bar',
                            smooth: true,
                            data: yesterdayNew,
                            itemStyle:{  
                                normal:{color:'#044D22'}  
                            } 
                        },
                        {
                            name:'当日催回案件数M1-',
                            type:'bar',
                            data:yesterdayPaid301,
                            itemStyle:{  
                                normal:{color:'#0B6E48'}  
                            } 
                        },
                        {
                            name:'当日催回案件数M1+',
                            type:'bar',
                            data:yesterdayPaid300,
                            itemStyle:{  
                                normal:{color:'#199475'}  
                            } 
                        },
                        {
                            name:'三日催回案件数',
                            type:'bar',
                            data:threeDayPaid,
                            itemStyle:{  
                                normal:{color:'#C7CEB2'}  
                            } 
                        },
                        {
                            name:'三日催回案件率',
                            type:'line',
                            yAxisIndex: 1,
                            data:NewPaidRate,
                            itemStyle:{  
                                normal:{color:'#E08031'}  
                            } 
                        }
                    ]
                };
                myChart.setOption(option);

                html_result = '' + 
                '<table class="table" style="width: 100%;margin:0 auto;"> '+
                    '<thead class="fixedThead" style="width: 100%"> '+
                        '<tr style="margin:0 auto;"><th>时间</th><th>当日新增案件数</th><th>当日催回案件数M1-</th><th>当日催回案件数M1+</th><th>三日催回案件数</th><th>三日催回案件率</th></tr>'+
                    '</thead> '+
                '<tbody class="scrollTbody" style="width: 100%;"> '
                lnum = times.length
                for (var i = 1; i <= lnum; i++)
                {
                    html_result += '<tr>';
                    html_result += '<td>'+times[lnum-i]+'</td>';
                    html_result += '<td>'+yesterdayNew[lnum-i]+'</td>';
                    html_result += '<td>'+yesterdayPaid301[lnum-i]+'</td>';
                    html_result += '<td>'+yesterdayPaid300[lnum-i]+'</td>';
                    html_result += '<td>'+threeDayPaid[lnum-i]+'</td>';
                    html_result += '<td>'+NewPaidRate[lnum-i]+"%"+'</td>';
                    html_result += '</tr>';
                }
                html_result += '</tbody> </table> '
                document.getElementById('data').innerHTML=html_result;
            }
        })
    }
});

});
