$(document).ready(function(){
    $.get("../api/v1/day?format=json&table=aeyegetrate&content=list",function(dataset){
        console.log(dataset);

        var myChart = echarts.init(document.getElementById('trend'));
        var tryNum = [];
        var sucNum = [];
        var sucRate = [];
        var times = [];
        for(i=0;i<dataset.length;i++)
        {
            tryNum.push(dataset[i]['tryNum']);
            sucNum.push(dataset[i]['sucNum']);
            sucRate.push(dataset[i]['sucRate']);
            times.push(dataset[i]['createDate']);
        }
        var option = {
            title : {
                text: '每日提现情况',
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
                data:['尝试提现','成功提现','成功提现率']
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
                    name:'尝试提现',
                    type:'line',
                    data:tryNum,
                    itemStyle:{  
                        normal:{color:'#f0ad4e'}  
                    } 
                },
                {
                    name:'成功提现',
                    type:'line',
                    data:sucNum,
                    itemStyle:{  
                        normal:{color:'#337ab7'}  
                    } 
                },
                {
                    name:'成功提现率',
                    type:'bar',
                    yAxisIndex: 1,
                    data:sucRate,
                    itemStyle:{  
                        normal:{color:'#5cb85c'}  
                    } 
                }
            ]
        };
        myChart.setOption(option);
    });
 });




