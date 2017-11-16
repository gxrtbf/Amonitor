$(document).ready(function(){
    $.getJSON("../static/data/flow/repaymentMoney.json",function(dataset){
        console.info(dataset)
        var l603 = [];
        var l605 = [];
        var l607 = [];
        var all = [];
        for(i=0;i<dataset['times'].length;i++)
        {
            l603.push(dataset['trend'][dataset['times'][i]]['603']);
            l605.push(dataset['trend'][dataset['times'][i]]['605']);
            l607.push(dataset['trend'][dataset['times'][i]]['607']);
            all.push(dataset['trend'][dataset['times'][i]]['repaidMoney']);
        }
        var labels = dataset['sum']['product'];
        labels.push('总金额');
        var myChart = echarts.init(document.getElementById('repaymentMoney'));
        var option = {
            title: {
                text: '还款金额曲线',
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
            series: [{
                name: '603',
                type: 'line',
                smooth: true,
                data: l603
            }, {
                name: '605',
                type: 'line',
                smooth: true,
                data: l605
            },{
                name: '607',
                type: 'line',
                smooth: true,
                data: l607
            },{
                name: '总金额',
                type: 'line',
                smooth: true,
                data: all
            }]
        };
        myChart.setOption(option);
    });
});