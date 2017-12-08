$(document).ready(function(){
    var cdata = {
        'table': "userincrease",
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
            var allow = [];
            var newApply = [];
            var oldApply = [];
            var register = [];
            var times = [];
            for(i=0;i<dataset.length;i++)
            {
                allow.push(dataset[i]['allow']);
                newApply.push(dataset[i]['newApply']);
                oldApply.push(dataset[i]['oldApply']);
                register.push(dataset[i]['register']);
                times.push(dataset[i]['createDate']);
            }
            var myChart = echarts.init(document.getElementById('increase'));
            var option = {
                title: {
                    text: '用户增长'
                    },
                tooltip : {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross',
                        label: {
                            backgroundColor: '#6a7985'
                            }
                        }
                    },
                    legend: {
                        data:['注册','申请(新)','申请(老)','授信']
                        },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                        },
                    xAxis : [
                                {
                                    type : 'category',
                                    boundaryGap : false,
                                    data : times
                                }
                        ],
                    yAxis : [
                            {
                                type : 'value'
                            }
                        ],
                    dataZoom: [{
                                type: 'inside',
                                start: 80,
                                end: 100
                            }, {
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
                    series : [
                                {
                                    name:'注册',
                                    type:'line',
                                    smooth: true,
                                    data:register
                                },
                                {
                                    name:'申请(新)',
                                    type:'line',
                                    smooth: true,
                                    data:newApply
                                },
                                {
                                    name:'申请(老)',
                                    type:'line',
                                    smooth: true,
                                    data:oldApply
                                },
                                {
                                    name:'授信',
                                    type:'line',
                                    smooth: true,
                                    data:allow
                                }
                            ]
                };
            myChart.setOption(option);
        }
    });
 });




