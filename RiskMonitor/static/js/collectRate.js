$(document).ready(function(){
    var cdata = {
        'table': "collectrate",
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
            var day4rate = [];
            var day7rate = [];
            var day15rate = [];
            var day30rate = [];
            var day60rate = [];
            var day90rate = [];
            var day90ratem = [];
            var times = [];

            lnum = dataset.length - 1
            for(i=0;i<dataset.length;i++)     
            {
                day4rate.push(dataset[lnum-i]['day4Rate']);
                day7rate.push(dataset[lnum-i]['day7Rate']);
                day15rate.push(dataset[lnum-i]['day15Rate']);
                day30rate.push(dataset[lnum-i]['day30Rate']);
                day60rate.push(dataset[lnum-i]['day60Rate']);
                day90rate.push(dataset[lnum-i]['day90Rate']);
                day90ratem.push(dataset[lnum-i]['day90Ratem']);

                times.push(dataset[lnum-i]['month'])
            }
            var myChart = echarts.init(document.getElementById('main'));
            var option = {
                title: {
                    text: '催回率',
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
                    data: '',
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
                series: [{
                    name: '4天催回率',
                    type: 'line',
                    smooth: true,
                    data: day4rate
                }, {
                    name: '7天催回率',
                    type: 'line',
                    smooth: true,
                    data: day7rate
                },{
                    name: '15天催回率',
                    type: 'line',
                    smooth: true,
                    data: day15rate
                },{
                    name: '30天催回率',
                    type: 'line',
                    smooth: true,
                    data: day30rate
                },{
                    name: '60天催回率',
                    type: 'line',
                    smooth: true,
                    data: day60rate
                },{
                    name: '90天催回率',
                    type: 'line',
                    smooth: true,
                    data: day90rate
                },{
                    name: '90天+催回率',
                    type: 'line',
                    smooth: true,
                    data: day90ratem
                }]
            };
            myChart.setOption(option);

            html_result = '' + 
            '<table class="table"> '+
            '<thead class="fixedThead"> '+
                '<tr><th>贷款月份</th><th>4天催回率</th><th>7天催回率</th><th>15天催回率</th><th>30天催回率</th><th>60天催回率</th><th>90天催回率</th><th>90天+催回率</th></tr> '+
            '</thead> '+
            '<tbody class="scrollTbody"> '
            lnum = times.length
            for (var i = 1; i <= lnum; i++)
            {
                html_result += '<tr>';
                html_result += '<th>'+times[lnum-i]+'</th>';
                html_result += '<th>'+day4rate[lnum-i]+'%'+'</th>';
                html_result += '<th>'+day7rate[lnum-i]+'%'+'</th>';
                html_result += '<th>'+day15rate[lnum-i]+'%'+'</th>';
                html_result += '<th>'+day30rate[lnum-i]+'%'+'</th>';
                html_result += '<th>'+day60rate[lnum-i]+'%'+'</th>';
                html_result += '<th>'+day90rate[lnum-i]+'%'+'</th>';
                html_result += '<th>'+day90ratem[lnum-i]+'%'+'</th>';
                html_result += '</tr>';
            }
            html_result += '</tbody> </table> '
            document.getElementById('data').innerHTML=html_result;
        }
    });
});