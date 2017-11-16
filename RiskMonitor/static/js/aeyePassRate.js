$(document).ready(function(){
    $.get("../api/index?format=json&table=aeyepassrate&content=list",function(dataset){
        console.log(dataset);

        var myChart = echarts.init(document.getElementById('trend'));
        var dayCheck = [];
        var dayPass = [];
        var passRate = [];
        var times = [];
        for(i=0;i<dataset.length;i++)
        {
            dayCheck.push(dataset[i]['applyNum']);
            dayPass.push(dataset[i]['passNum']);
            passRate.push(dataset[i]['passRate']);
            times.push(dataset[i]['createDate']);
        }
        var option = {
            title : {
                text: '每日审核情况',
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
            toolbox: {
                feature: {
                    dataView: {show: true, readOnly: false},
                    magicType: {show: true, type: ['line', 'bar']},
                    restore: {show: true},
                    saveAsImage: {show: true}
                }
            },
            legend: {
                data:['审核量','通过量','通过率']
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
                },
                {
                    type: 'value',
                    name: '通过率%',
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
                    name:'审核量',
                    type:'line',
                    data:dayCheck,
                    itemStyle:{  
                        normal:{color:'blue'}  
                    } 
                },
                {
                    name:'通过量',
                    type:'line',
                    data:dayPass,
                    itemStyle:{  
                        normal:{color:'green'}  
                    } 
                },
                {
                    name:'通过率',
                    type:'bar',
                    yAxisIndex: 1,
                    data:passRate,
                    itemStyle:{  
                        normal:{color:'#f0ad4e'}  
                    } 
                }
            ]
        };
        myChart.setOption(option);
    });
 });




