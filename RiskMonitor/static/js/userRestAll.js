$(document).ready(function(){
    var nt = CurentDate();
    var cdata = {
        'table': "userrest",
        'content': "list",
        'para': [
            {
                'key': "currentDate",
                'value': nt[0],
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
            console.log(dataset);
            var datatemp = [[], [], [], [], [], []];
            for(i=0;i<nt.length;i++)
            {
                for(j=0;j<dataset.length;j++)
                {
                    dicttemp = dataset[j]
                    if(dicttemp['currentDate']==nt[i])
                    {
                        datatemp[i].push(dicttemp['currentActive'])
                    }
                }
            };
            seriestemp = []
            for(i=0;i<nt.length;i++)
            {
                dtc = {
                    name: nt[i],
                    type: 'bar',
                    stack: '活跃量',
                    data: datatemp[i]
                };
                seriestemp.push(dtc);
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
                    data: '活跃量'
                },
                xAxis: [
                    {
                        type: 'category',
                        data: nt,
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
                    }
                ],
                series: seriestemp
            };
            myChart.setOption(option);
        }
    });
});

function CurentDate()
{ 
    var now = new Date();
    var nlist = [];
    var ml = [-4,-3,-2,-1,0,1];

    for(i=0;i<ml.length;i++)
    {
        var year = now.getFullYear();
        var month = now.getMonth() + ml[i];
        if(month < 1)
        {
            year = year - 1
            month = month + 12
        }
        if(month < 10)
        {
            clockc = year + "-0" + month;
        }
        else
        {
            clockc = year + "-" + month;
        }
        nlist.push(clockc)
    }
    return(nlist); 
} 

