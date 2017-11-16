$(document).ready(function(){
    $.getJSON("../static/data/flow/incomeMoney.json",function(dataset){
        console.log(dataset)
        var s101 = [];
        var s102 = [];
        var s103 = [];
        var s104 = [];
        var j1 = [];
        var s0 = [];
        var sp3 = [];
        var s2 = [];
        var s5 = [];
        var xj4 = [];
        var s6 = [];
        var all = [];
        for(i=0;i<dataset['times'].length;i++)
        {
            s101.push(dataset['trend'][dataset['times'][i]]['闪电贷101']);
            s102.push(dataset['trend'][dataset['times'][i]]['闪电贷102']);
            s103.push(dataset['trend'][dataset['times'][i]]['闪电贷103']);
            s104.push(dataset['trend'][dataset['times'][i]]['闪电贷104']);
            s0.push(dataset['trend'][dataset['times'][i]]['闪电贷0']);
            s2.push(dataset['trend'][dataset['times'][i]]['闪电贷2']);
            s5.push(dataset['trend'][dataset['times'][i]]['闪电贷5']);
            s6.push(dataset['trend'][dataset['times'][i]]['闪电贷6']);
            j1.push(dataset['trend'][dataset['times'][i]]['及时雨1']);
            sp3.push(dataset['trend'][dataset['times'][i]]['商品贷3']);
            xj4.push(dataset['trend'][dataset['times'][i]]['现金分期4']);
            all.push(dataset['trend'][dataset['times'][i]]['allIncome']);
        }
        var labels = dataset['sum']['product'];
        labels.push('总金额');
        var myChart = echarts.init(document.getElementById('income'));
        var option = {
            title: {
                text: '',
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
                data: labels,
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
                data: dataset['times']
            }],
            yAxis: [{
                type: 'value',
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
                    name: '闪电贷102',
                    type: 'line',
                    smooth: true,
                    data: s102
                },
                {
                    name: '闪电贷103',
                    type: 'line',
                    smooth: true,
                    data: s103
                },
                {
                    name: '闪电贷101',
                    type: 'line',
                    smooth: true,
                    data: s101
                },
                {
                    name: '闪电贷104',
                    type: 'line',
                    smooth: true,
                    data: s104
                },
                {
                    name: '及时雨1',
                    type: 'line',
                    smooth: true,
                    data: j1
                },
                {
                    name: '闪电贷0',
                    type: 'line',
                    smooth: true,
                    data: s0
                },
                {
                    name: '商品贷3',
                    type: 'line',
                    smooth: true,
                    data: sp3
                },
                {
                    name: '闪电贷2',
                    type: 'line',
                    smooth: true,
                    data: s2
                },
                {
                    name: '闪电贷5',
                    type: 'line',
                    smooth: true,
                    data: s5
                },
                {
                    name: '现金分期4',
                    type: 'line',
                    smooth: true,
                    data: xj4
                },
                {
                    name: '闪电贷6',
                    type: 'line',
                    smooth: true,
                    data: s6
                },
                {
                    name: '总金额',
                    type: 'line',
                    smooth: true,
                    data: all
                }
            ]
        };
        myChart.setOption(option);

        var myChart = echarts.init(document.getElementById('sumIncome'));
        option = {
            title : {
                text: '不同产品贷款笔数占比情况',
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
                data:dataset['label']
            },
            toolbox: {
                show : true,
                feature : {
                    mark : {show: true},
                    dataView : {show: true, readOnly: false},
                    magicType : {
                        show: true,
                        type: dataset['label']
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
                    data:[
                        {value:dataset['sum']['num'][0], name:'闪电贷102'},
                        {value:dataset['sum']['num'][1], name:'闪电贷103'},
                        {value:dataset['sum']['num'][2], name:'闪电贷101'},
                        {value:dataset['sum']['num'][3], name:'闪电贷104'},
                        {value:dataset['sum']['num'][4], name:'及时雨1'},
                        {value:dataset['sum']['num'][5], name:'闪电贷0'},
                        {value:dataset['sum']['num'][6], name:'商品贷3'},
                        {value:dataset['sum']['num'][7], name:'闪电贷2'},
                        {value:dataset['sum']['num'][8], name:'闪电贷5'},
                        {value:dataset['sum']['num'][9], name:'现金分期4'},
                        {value:dataset['sum']['num'][10], name:'闪电贷6'},
                    ]
                }
            ]
        };
        myChart.setOption(option);
    });
});