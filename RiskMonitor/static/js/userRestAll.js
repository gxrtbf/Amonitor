$(document).ready(function(){
    var cdata = {
        'table': "userrest",
        'content': "list",
        'para': [
            {
                'key': "registerDate",
                'value': "2017-09",
                'way': "gte"
            }
        ]
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
            var allPass = [];
            var currentActive = [];
            var currentActiveRate = [];
            var times = [];
            for(i=0;i<dataset.length;i++)
            {
                allPass.push(dataset[i]['allPass']);
                currentActive.push(dataset[i]['currentActive']);
                currentActiveRate.push(dataset[i]['currentActiveRate']);
                times.push(dataset[i]['currentDate']);
            }
            var myChart = echarts.init(document.getElementById('main'));
            var option = {
                title : {
                    text: '用户留存比较',
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross',
                        crossStyle: {
                            color: '#999'
                        }
                    }
                },
                legend: {
                    data:['总通过量','活跃量','活跃率']
                },
                xAxis: [
                    {
                        type: 'category',
                        data: times,
                        axisPointer: {
                            type: 'shadow'
                        }
                    }
                ],
                yAxis: [
                    {
                        type: 'value',
                        name: '活跃率%',
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
                        name: '数量',
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
                        start: 20,
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
                        name:'总通过量',
                        type:'bar',
                        yAxisIndex: 1,
                        data:allPass,
                        itemStyle:{  
                            normal:{color:'#337ab7'}  
                        } 
                    },
                    {
                        name:'活跃量',
                        type:'bar',
                        yAxisIndex: 1,
                        data:currentActive,
                        itemStyle:{  
                            normal:{color:'#5cb85c'}  
                        } 
                    },
                    {
                        name:'活跃率',
                        type:'line',
                        yAxisIndex: 0,
                        data:currentActiveRate,
                        itemStyle:{  
                            normal:{color:'#f0ad4e'}  
                        } 
                    }
                ]
            };
            myChart.setOption(option);
        }
    });
});

