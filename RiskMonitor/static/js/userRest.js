$(document).ready(function(){
    reflashdata()
});

function reflashdata() {
    var year = document.getElementById("year_span").innerText;
    var month = document.getElementById("month_span").innerText;

    var sdate = year +'-'+ month;

    var charttitle =  '注册用户留存情况(' + year + '.' + month + ')'

    $.get("../api/v1/day?format=json&table=userrest&content=list&registerDate="+sdate,function(dataset){
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
                text: charttitle,
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

        html_result = '' + 
        '<table class="table" style="width: 100%;margin:0 auto;"> '+
            '<thead class="fixedThead" style="width: 100%"> '+
                '<tr style="margin:0 auto;"><th>月份</th><th>总通过人数</th><th>活跃人数</th><th>活跃率</th>' +
            '</thead> '+
        '<tbody class="scrollTbody" style="width: 100%;"> '
        lnum = times.length
        for (var i = 1; i <= lnum; i++)
        {
            html_result += '<tr>';
            html_result += '<td>'+times[lnum-i]+'</td>';
            html_result += '<td>'+allPass[lnum-i]+'</td>';
            html_result += '<td>'+currentActive[lnum-i]+'</td>';
            html_result += '<td>'+currentActiveRate[lnum-i]+'%</td>';
            html_result += '</tr>';
        }
        html_result += '</tbody> </table> '
        document.getElementById('data').innerHTML=html_result;
    }); 
};

$(function(){   
    $('#year li a').click(function(){
        var thisToggle = $(this).is('.sizeyear') ? $(this) : $(this).prev();
        var checkBox = thisToggle.prev();
        checkBox.trigger('click');
        $('.sizeyear').removeClass('current');
        thisToggle.addClass('current');
        return false;
    }); 
    $('#month li a').click(function(){
        var thisToggle = $(this).is('.sizemonth') ? $(this) : $(this).prev();
        var checkBox = thisToggle.prev();
        checkBox.trigger('click');
        $('.sizemonth').removeClass('current');
        thisToggle.addClass('current');
        return false;
    }); 
});
$("#year li a").click(function(){
    var text = $(this).html();
    $(".year span").html(text);
    console.log($("#date").find(".year span.value").html())
});
$("#month li a").click(function(){
    var text = $(this).html();
    $(".month span").html(text);
    console.log($("#date").find(".month span.value").html())
});

$("#searchdata").click(function(){
    reflashdata()
});


