$(document).ready(function(){
    function getQueryString(name){
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return decodeURI(r[2]); return null;
    };
    var fundId = getQueryString('fundId');
    if(!fundId){
        fundId = '快乐达连连账户'
    }
    $.get("../api/v1/day?format=json&table=flowloanfund&content=item&fundName=" + fundId,function(dataset){
        console.log(dataset);
        document.getElementById("fundId").innerHTML = '业务-贷款金额-' + fundId;

        var delay0 = [];
        var times = [];

        for(i=0;i<dataset.length;i++){
            delay0.push(dataset[i]['sumMoney']);
            times.push(dataset[i]['createDate']);
        }

        var myChart = echarts.init(document.getElementById('main'));
        var option = {
            title: {
                text: '日贷款金额',
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
                data: ['日贷款金额'],
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
                name: '日贷款金额',
                type: 'bar',
                smooth: true,
                data: delay0
            }]
        };
        myChart.setOption(option);
    });

    $.get("../api/v1/day?format=json&table=flowdelayrateno&content=item&fundName=" + fundId,function(dataset){
        console.log(dataset)
        var myChart = echarts.init(document.getElementById('main1'));
        var delayOld = [];
        var delayNew = [];
        var times = [];
        for(i=0;i<dataset.length;i++){
            delayOld.push(dataset[i]['oldDelayRate3']);
            delayNew.push(dataset[i]['newDelayRate3']);
            times.push(dataset[i]['createDate']);
        }
        var option = {
            title: {
                text: '新老逾期率3+',
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
                data: ['逾期率3+(新)','逾期率3+(老)'],
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
                name: '逾期率3+(新)',
                type: 'line',
                smooth: true,
                data: delayNew
            },
            {
                name: '逾期率3+(老)',
                type: 'line',
                smooth: true,
                data: delayOld
            }]
        }
        myChart.setOption(option);
    });
 });




