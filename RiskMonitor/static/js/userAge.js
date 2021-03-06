$(document).ready(function(){
    var cdata = {
        'table': "userage",
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
            var age1 = [];
            var age2 = [];
            var age3 = [];
            var age4 = [];
            var age5 = [];
            var times = [];
            for(i=0;i<dataset.length;i++)
            {
                age1.push(dataset[i]['age1']);
                age2.push(dataset[i]['age2']);
                age3.push(dataset[i]['age3']);
                age4.push(dataset[i]['age4']);
                age5.push(dataset[i]['age5']);
                times.push(dataset[i]['createDate']);
            }

            var myChart = echarts.init(document.getElementById('main'));
            var option = {
                title: {
                    text: '用户增长',
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
                    data: ['18岁及以下','19-25岁','26-33岁','34-41岁','42岁及以上'],
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
                    name: '18岁及以下',
                    type: 'line',
                    smooth: true,
                    data: age1
                },
                {
                    name: '19-25岁',
                    type: 'line',
                    smooth: true,
                    data: age2
                },
                {
                    name: '26-33岁',
                    type: 'line',
                    smooth: true,
                    data: age3
                },
                {
                    name: '34-41岁',
                    type: 'line',
                    smooth: true,
                    data: age4
                },
                {
                    name: '42岁及以上',
                    type: 'line',
                    smooth: true,
                    data: age5
                }]
            };
            myChart.setOption(option);
        }
    });
    var cdata = {
        'table': "userageall",
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
            var myChart = echarts.init(document.getElementById('loudou'));
            var option = {
                title : {
                    text: '年龄占比情况',
                    // subtext: '纯属虚构',
                    x:'center'
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{b} : {c} ({d}%)"
                },
                legend: {
                    x : 'center',
                    y : 'bottom',
                    data:dataset['age']
                },
                toolbox: {
                    show : true,
                    feature : {
                        mark : {show: true},
                        dataView : {show: true, readOnly: false},
                        magicType : {
                            show: true,
                            type: ['18岁及以下','19-25岁','26-33岁','34-41岁','42岁及以上']
                        },
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                series : [
                    {
                        name:'面积模式',
                        type:'pie',
                        radius : [40, 100],
                        center : ['50%', '50%'],
                        roseType : 'radius',
                        data:[
                            {value:dataset[0]['age1'], name:'18岁及以下'},
                            {value:dataset[0]['age2'], name:'19-25岁'},
                            {value:dataset[0]['age3'], name:'26-33岁'},
                            {value:dataset[0]['age4'], name:'34-41岁'},
                            {value:dataset[0]['age5'], name:'42岁及以上'},
                        ]
                    }
                ]
            };
            myChart.setOption(option);
        }
    });
});