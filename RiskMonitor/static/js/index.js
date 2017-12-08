$(document).ready(function(){
    function formatNumberRgx(num) {  
      var parts = num.toString().split(".");  
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");  
      return parts.join(".");  
    };
    var cdata = {
        'table': "indexhead",
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
            document.getElementById("sumUser").innerHTML = formatNumberRgx(dataset[0]["sumUser"]);
            document.getElementById("activeUser").innerHTML = formatNumberRgx(dataset[0]["activeUser"]);
            document.getElementById("tradeNum").innerHTML = formatNumberRgx(dataset[0]["tradeNum"]);
            document.getElementById("tradeMoney").innerHTML = formatNumberRgx(dataset[0]["tradeMoney"]);
    }
    });
    var cdata = {
        'table': "indexdash",
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
            var myChart = echarts.init(document.getElementById('dashbook3'));
            var option = {
                title: {
                    text: '日均综合服务费',
                    left: 'center',
                },
                tooltip : {
                    formatter: "{a} <br/>{c} {b}"
                },
                series : [
                    {
                        name: '日均综合服务费',
                        type: 'gauge',
                        center: ['50%', '55%'],    // 默认全局居中
                        radius: '60%',
                        min:0,
                        max:300,
                        endAngle:45,
                        axisLine: {            // 坐标轴线
                            lineStyle: {       // 属性lineStyle控制线条样式
                                width: 8
                            }
                        },
                        axisTick: {            // 坐标轴小标记
                            length:12,        // 属性length控制线长
                            lineStyle: {       // 属性lineStyle控制线条样式
                                color: 'auto'
                            }
                        },
                        splitLine: {           // 分隔线
                            length:20,         // 属性length控制线长
                            lineStyle: {       // 属性lineStyle（详见lineStyle）控制线条样式
                                color: 'auto'
                            }
                        },
                        pointer: {
                            width:5
                        },
                        title: {
                            offsetCenter: [0, '-30%'],       // x, y，单位px
                        },
                        detail: {
                            textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                                fontWeight: 'bolder'
                            }
                        },
                        data:[{value: dataset[0]['avgServiceMoney'], name: '￥/笔'}]
                    }
                ]
            };
            myChart.setOption(option);
            var myChart = echarts.init(document.getElementById('dashbook1'));
            var option = {
                title: {
                    text: '平均贷款期数',
                    left: 'center',
                },
                tooltip : {
                    formatter: "{a} <br/>{c} {b}"
                },
                series : [
                    {
                        name: '平均贷款期数',
                        type: 'gauge',
                        center: ['50%', '55%'],    // 默认全局居中
                        radius: '60%',
                        min:0,
                        max:30,
                        endAngle:45,
                        axisLine: {            // 坐标轴线
                            lineStyle: {       // 属性lineStyle控制线条样式
                                width: 8
                            }
                        },
                        axisTick: {            // 坐标轴小标记
                            length:12,        // 属性length控制线长
                            lineStyle: {       // 属性lineStyle控制线条样式
                                color: 'auto'
                            }
                        },
                        splitLine: {           // 分隔线
                            length:20,         // 属性length控制线长
                            lineStyle: {       // 属性lineStyle（详见lineStyle）控制线条样式
                                color: 'auto'
                            }
                        },
                        pointer: {
                            width:5
                        },
                        title: {
                            offsetCenter: [0, '-30%'],       // x, y，单位px
                        },
                        detail: {
                            textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                                fontWeight: 'bolder'
                            }
                        },
                        data:[{value: dataset[0]['avgTermNum'], name: '天/人'}]
                    }
                ]
            };
            myChart.setOption(option);
            var myChart = echarts.init(document.getElementById('dashbook2'));
            var option = {
                title: {
                    text: '平均借贷金额',
                    left: 'center',
                },
                tooltip : {
                    formatter: "{a} <br/>{c} {b}"
                },
                series : [
                    {
                        name: '平均借贷金额',
                        type: 'gauge',
                        z: 3,
                        min: 0,
                        max: 3000,
                        radius: '60%',
                        axisLine: {            // 坐标轴线
                            lineStyle: {       // 属性lineStyle控制线条样式
                                width: 10
                            }
                        },
                        axisTick: {            // 坐标轴小标记
                            length: 15,        // 属性length控制线长
                            lineStyle: {       // 属性lineStyle控制线条样式
                                color: 'auto'
                            }
                        },
                        splitLine: {           // 分隔线
                            length: 20,         // 属性length控制线长
                            lineStyle: {       // 属性lineStyle（详见lineStyle）控制线条样式
                                color: 'auto'
                            }
                        },
                        title : {
                            textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                                fontWeight: 'bolder',
                                fontSize: 20,
                                fontStyle: 'italic'
                            }
                        },
                        detail : {
                            textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                                fontWeight: 'bolder'
                            }
                        },
                        data:[{value: dataset[0]['avgMoney'], name: '￥/笔'}]
                    }
                ]
            };
            myChart.setOption(option);
        }
    });
    var cdata = {
        'table': "indexhopper",
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
            var percent = new Array();
            for(var key in dataset[0]){
                percent[key] = (dataset[0][key]/(dataset[0]['register'])*100).toFixed(2)
            }
            var myChart = echarts.init(document.getElementById('loudou'));
            // var dataset = {'注册':'710000','申请':'690000','授信':'70000','活跃':'60000','复借':'20000'}
            var option = {
                title: {
                    text: '转化',
                    // subtext: '纯属虚构'
                },
                tooltip: {
                    trigger: 'item',
                    formatter: function(a){
                                    return a['data']['name'] + ':' + dataset[0][a['data']['label']]
                                }
                },
                legend: {
                    data: ['注册','申请','授信','出贷','复借']
                },
                calculable: true,
                series: [
                    {
                        name:'用户转化情况',
                        type:'funnel',
                        left: '10%',
                        top: 60,
                        bottom: 60,
                        width: '80%',
                        min: 0,
                        max: 5,
                        minSize: '0%',
                        maxSize: '100%',
                        sort: 'descending',
                        gap: 2,
                        label: {
                            normal: {
                                show: true,
                                position: 'inside',
                                formatter: function(a){
                                    return a['data']['name'] + ':' + percent[a['data']['label']] + '%'
                                }
                            },
                            emphasis: {
                                textStyle: {
                                    fontSize: 20
                                }
                            }
                        },
                        labelLine: {
                            normal: {
                                length: 10,
                                lineStyle: {
                                    width: 1,
                                    type: 'solid'
                                }
                            }
                        },
                        itemStyle: {
                            normal: {
                                borderColor: '#fff',
                                borderWidth: 1
                            }
                        },
                        data: [
                            {value: 5, name: '注册', label: 'register'},
                            {value: 4, name: '申请', label: 'applys'},
                            {value: 3, name: '授信', label: 'passs'},
                            {value: 2, name: '出贷', label: 'loan'},
                            {value: 1, name: '复借', label: 'reloan'}
                        ]
                    }
                ]
            };
            myChart.setOption(option);
        }
    });
    var cdata = {
        'table': "indexacrepay",
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
            var acRepayMoney = [];
            var noRepayMoney = [];
            var repayRate = [];
            var times = [];
            for(i=0;i<dataset.length;i++)
            {
                acRepayMoney.push(dataset[i]['acRepayMoney']);
                noRepayMoney.push(dataset[i]['allRepayMoney']-dataset[i]['acRepayMoney']);
                repayRate.push(dataset[i]['repayRate']);
                times.push(dataset[i]['createDate']);
            }
            var myChart = echarts.init(document.getElementById('main'));
            var option = {
                title: {
                    text: '每日还款情况(金额)'
                },
                tooltip : {
                    trigger: 'axis',
                    axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                        type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                    }
                },
                legend: {
                    data:['未还金额','实还金额','还款比例(金额)']
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
                        data : times
                    }
                ],
                yAxis : [
                    {
                        type : 'value'
                    },
                    {
                        type: 'value',
                        name: '还款率%',
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
                        name:'未还金额',
                        type:'bar',
                        stack: '应还金额',
                        itemStyle:{
                            normal:{
                                color:'#d9534f',
                            },
                        },
                        data:noRepayMoney
                    },
                    {
                        name:'实还金额',
                        type:'bar',
                        stack: '应还金额',
                        itemStyle:{
                            normal:{
                                color:'#5cb85c',
                            },
                        },
                        data:acRepayMoney
                    },
                    {
                        name:'还款比例(金额)',
                        type:'line',
                        yAxisIndex: 1,
                        data:repayRate,
                        itemStyle:{  
                            normal:{color:'#f0ad4e'}  
                        } 
                    }
                ]
            };
            myChart.setOption(option);
        }
    });
    var cdata = {
        'table': "indexcity",
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
            var city = new Array();
            for(i=0;i<dataset.length;i++){
                city[dataset[i]['cityName']] = dataset[i]['numInCity']
            }
            var data = [
                {
                    name: "郴州",
                    value: city["郴州"]
                },
                {
                    name: "南充",
                    value: city["南充"]
                },
                {
                    name: "汕尾",
                    value: city["汕尾"]
                },
                {
                    name: "长治",
                    value: city["长治"]
                },
                {
                    name: "漳州",
                    value: city["漳州"]
                },
                {
                    name: "莆田",
                    value: city["莆田"]
                },
                {
                    name: "汕头",
                    value: city["汕头"]
                },
                {
                    name: "百色",
                    value: city["百色"]
                },
                {
                    name: "湛江",
                    value: city["湛江"]
                },
                {
                    name: "荆州",
                    value: city["荆州"]
                },
                {
                    name: "清远",
                    value: city["清远"]
                },
                {
                    name: "内江",
                    value: city["内江"]
                },
                {
                    name: "梅州",
                    value: city["梅州"]
                },
                {
                    name: "怀化",
                    value: city["怀化"]
                },
                {
                    name: "绵阳",
                    value: city["绵阳"]
                },
                {
                    name: "潮州",
                    value: city["潮州"]
                },
                {
                    name: "常德",
                    value: city["常德"]
                },
                {
                    name: "云浮",
                    value: city["云浮"]
                },
                {
                    name: "龙岩",
                    value: city["龙岩"]
                },
                {
                    name: "重庆",
                    value: city["重庆"]
                },
                {
                    name: "黄冈",
                    value: city["黄冈"]
                },
                {
                    name: "揭阳",
                    value: city["揭阳"]
                },
                {
                    name: "钦州",
                    value: city["钦州"]
                },
                {
                    name: "福州",
                    value: city["福州"]
                },
                {
                    name: "泸州",
                    value: city["泸州"]
                },
                {
                    name: "赣州",
                    value: city["赣州"]
                },
                {
                    name: "广安",
                    value: city["广安"]
                },
                {
                    name: "茂名",
                    value: city["茂名"]
                },
                {
                    name: "韶关",
                    value: city["韶关"]
                },
                {
                    name: "河池",
                    value: city["河池"]
                },
                {
                    name: "盐城",
                    value: city["盐城"]
                },
                {
                    name: "毕节",
                    value: city["毕节"]
                },
                {
                    name: "海南省",
                    value: city["海南省"]
                },
                {
                    name: "淮安",
                    value: city["淮安"]
                },
                {
                    name: "河源",
                    value: city["河源"]
                },
                {
                    name: "遂宁",
                    value: city["遂宁"]
                },
                {
                    name: "南宁",
                    value: city["南宁"]
                },
                {
                    name: "泉州",
                    value: city["泉州"]
                },
                {
                    name: "邯郸",
                    value: city["邯郸"]
                },
                {
                    name: "恩施土家族苗族自治州",
                    value: city["恩施土家族苗族自治州"]
                },
                {
                    name: "玉林",
                    value: city["玉林"]
                },
                {
                    name: "保定",
                    value: city["保定"]
                },
                {
                    name: "肇庆",
                    value: city["肇庆"]
                },
                {
                    name: "衡阳",
                    value: city["衡阳"]
                },
                {
                    name: "桂林",
                    value: dataset["桂林"]
                },
                {
                    name: "德阳",
                    value: city["德阳"]
                },
                {
                    name: "江门",
                    value: city["江门"]
                },
                {
                    name: "武汉",
                    value: city["武汉"]
                },
                {
                    name: "周口",
                    value: city["周口"]
                },
                {
                    name: "成都",
                    value: city["成都"]
                },
                {
                    name: "南通",
                    value: city["南通"]
                },
                {
                    name: "安庆",
                    value: city["安庆"]
                },
                {
                    name: "广州",
                    value: city["广州"]
                },
                {
                    name: "柳州",
                    value: city["柳州"]
                },
                {
                    name: "阜阳",
                    value: city["阜阳"]
                },
                {
                    name: "温州",
                    value: city["温州"]
                },
                {
                    name: "岳阳",
                    value: city["岳阳"]
                },
                {
                    name: "梧州",
                    value: city["梧州"]
                },
                {
                    name: "上饶",
                    value: city["上饶"]
                },
                {
                    name: "达川",
                    value: city["达川"]
                },
                {
                    name: "徐州",
                    value: city["徐州"]
                },
                {
                    name: "渭南",
                    value: city["渭南"]
                },
                {
                    name: "邵阳",
                    value: city["邵阳"]
                },
                {
                    name: "宜宾",
                    value: city["宜宾"]
                },
                {
                    name: "贵港",
                    value: city["贵港"]
                },
                {
                    name: "巴中",
                    value: city["巴中"]
                },
                {
                    name: "永州",
                    value: city["永州"]
                },
                {
                    name: "宁德",
                    value: city["宁德"]
                },
                {
                    name: "遵义",
                    value: city["遵义"]
                },
                {
                    name: "惠州",
                    value: city["惠州"]
                },
                {
                    name: "湖北省",
                    value: city["湖北省"]
                }
            ];

            var geoCoordMap = {
                "郴州": [
                    113.014717,
                    25.770509
                ],
                "南充": [
                    106.110698,
                    30.837793
                ],
                "汕尾": [
                    115.375158,
                    22.786186
                ],
                "长治": [
                    113.116404,
                    36.195409
                ],
                "漳州": [
                    117.647093,
                    24.513025
                ],
                "淮安": [
                    119.113185,
                    33.551052
                ],
                "汕头": [
                    116.681972,
                    23.354091
                ],
                "百色": [
                    106.618283,
                    23.902479
                ],
                "湛江": [
                    110.359368,
                    21.270702
                ],
                "荆州": [
                    112.239631,
                    30.335237
                ],
                "清远": [
                    113.056042,
                    23.681774
                ],
                "内江": [
                    105.058433,
                    29.580228
                ],
                "梅州": [
                    116.122523,
                    24.288578
                ],
                "怀化": [
                    110.001922,
                    27.569517
                ],
                "钦州": [
                    108.654146,
                    21.979933
                ],
                "潮州": [
                    116.622756,
                    23.656703
                ],
                "常德": [
                    111.698784,
                    29.031654
                ],
                "云浮": [
                    112.044491,
                    22.915094
                ],
                "莆田": [
                    119.007777,
                    25.454084
                ],
                "重庆": [
                    106.912251,
                    29.4315861
                ],
                "南宁": [
                    108.366543,
                    22.817002
                ],
                "遵义": [
                    106.927389,
                    27.725654
                ],
                "绵阳": [
                    104.679004,
                    31.46746
                ],
                "南通": [
                    120.894291,
                    31.980171
                ],
                "福州": [
                    119.296482,
                    26.074478
                ],
                "巴中": [
                    106.747477,
                    31.867903
                ],
                "泸州": [
                    105.44174,
                    28.871569
                ],
                "赣州": [
                    114.933546,
                    25.830694
                ],
                "揭阳": [
                    116.372708,
                    23.549701
                ],
                "茂名": [
                    110.925439,
                    21.662991
                ],
                "河池": [
                    108.085261,
                    24.692931
                ],
                "盐城": [
                    120.16366,
                    33.347316
                ],
                "毕节": [
                    105.291643,
                    27.283955
                ],
                "龙岩": [
                    117.017536,
                    25.075123
                ],
                "广安": [
                    106.633088,
                    30.456224
                ],
                "黄冈": [
                    114.872199,
                    30.453667
                ],
                "泉州": [
                    118.675675,
                    24.874132
                ],
                "遂宁": [
                    105.592898,
                    30.532847
                ],
                "河源": [
                    114.700961,
                    23.743685
                ],
                "恩施土家族苗族自治州": [
                    109.488172,
                    30.272156
                ],
                "玉林": [
                    110.18122,
                    22.654032
                ],
                "保定": [
                    115.464589,
                    38.874434
                ],
                "肇庆": [
                    112.465091,
                    23.047191
                ],
                "衡阳": [
                    112.572018,
                    26.893368
                ],
                "桂林": [
                    110.179953,
                    25.234479
                ],
                "海南省": [
                    109.949686,
                    19.5663947
                ],
                "江门": [
                    113.081508,
                    22.579117
                ],
                "武汉": [
                    114.305539,
                    30.592849
                ],
                "周口": [
                    114.69695,
                    33.626149
                ],
                "成都": [
                    104.066801,
                    30.572815
                ],
                "邯郸": [
                    114.538961,
                    36.625656
                ],
                "安庆": [
                    117.115101,
                    30.531919
                ],
                "广州": [
                    113.264385,
                    23.12911
                ],
                "柳州": [
                    109.428608,
                    24.326292
                ],
                "阜阳": [
                    115.814504,
                    32.890479
                ],
                "温州": [
                    120.699361,
                    27.993828
                ],
                "岳阳": [
                    113.12873,
                    29.356803
                ],
                "梧州": [
                    111.279115,
                    23.476962
                ],
                "上饶": [
                    117.943433,
                    28.454862
                ],
                "达川": [
                    107.511843,
                    31.196079
                ],
                "徐州": [
                    117.284124,
                    34.205768
                ],
                "渭南": [
                    109.502882,
                    34.49938
                ],
                "邵阳": [
                    111.467674,
                    27.23895
                ],
                "宜宾": [
                    104.643159,
                    28.751836
                ],
                "贵港": [
                    109.598926,
                    23.11153
                ],
                "韶关": [
                    113.59762,
                    24.810879
                ],
                "永州": [
                    111.613445,
                    26.420394
                ],
                "宁德": [
                    119.547932,
                    26.665617
                ],
                "德阳": [
                    104.397894,
                    31.126855
                ],
                "惠州": [
                    114.415801,
                    23.112257
                ],
                "湖北省": [
                    112.2384017,
                    30.7378118
                ]
            };

            var convertData = function(data) {
                var res = [];
                for (var i = 0; i < data.length; i++) {
                    var geoCoord = geoCoordMap[data[i].name];
                    if (geoCoord) {
                        res.push({
                            name: data[i].name,
                            value: geoCoord.concat(data[i].value)
                        });
                    }
                }
                return res;
            };

            var convertedData = [
                convertData(data),
                convertData(data.sort(function(a, b) {
                    return b.value - a.value;
                }).slice(0, 6))
            ];
            data.sort(function(a, b) {
                return a.value - b.value;
            })

            var selectedItems = [];
            var categoryData = [];
            var barData = [];
            //   var maxBar = 30;
            var sum = 0;
            var count = data.length;
            for (var i = 0; i < data.length; i++) {
                categoryData.push(data[i].name);
                barData.push(data[i].value);
                sum += data[i].value;
            }

            var option = {
                backgroundColor: '#FFFFFF',
                animation: true,
                animationDuration: 1000,
                animationEasing: 'cubicInOut',
                animationDurationUpdate: 1000,
                animationEasingUpdate: 'cubicInOut',
                title: [{
                    text: '贷款用户地区分布',
                    // link: 'http://pages.anjuke.com/expert/newexpert.html',
                    // subtext: 'data from Anjuke',
                    // sublink: 'http://pages.anjuke.com/expert/newexpert.html',
                    left: 'center',
                    y: 50,
                    textStyle: {
                        color: '#000',
                        fontSize: 30
                    }
                }],
                brush: {
                    outOfBrush: {
                        color: '#abc'
                    },
                    brushStyle: {
                        borderWidth: 2,
                        color: 'rgba(0,0,0,0.2)',
                        borderColor: 'rgba(0,0,0,0.5)',
                    },
                    seriesIndex: [0, 1],
                    throttleType: 'debounce',
                    throttleDelay: 300,
                    geoIndex: 0
                },
                geo: {
                    map: 'china',
                    left: '10',
                    right: '35%',
                    center: [93, 36.2],
                    zoom: 1.5,
                    label: {
                        emphasis: {
                            show: false
                        }
                    },
                    roam: true,
                    itemStyle: {
                        normal: {
                            shadowBlur: 20,
                            shadowColor: 'rgba(0, 0, 0,0.8)',
                            areaColor: '#004571',
                            borderColor: '#6AC6E6'
                        },
                        emphasis: {
                            areaColor: '#00385E'
                        }
                    }
                },
                tooltip: {
                    trigger: 'item',
                    formatter: function(a){
                        return a['data']['name'] + ":" + a['data']['value'][2]
                    }
                },
                grid: {
                    right: 40,
                    top: 100,
                    bottom: 40,
                    width: '30%'
                },
                series: [{
                    // name: 'pm2.5',
                    type: 'scatter',
                    coordinateSystem: 'geo',
                    data: convertedData[0],
                    symbolSize: function(val) {
                        return Math.max(val[2] / 50, 8);
                    },
                    label: {
                        normal: {
                            formatter: '',
                            position: 'right',
                            show: false
                        },
                        emphasis: {
                            show: false
                        }
                    },
                    itemStyle: {
                        normal: {
                            color: '#FF8C00',
                            position: 'right',
                            show: true
                        }
                    }
                }, {
                    //  name: 'Top 5',
                    type: 'effectScatter',
                    coordinateSystem: 'geo',
                    data: convertedData[0],
                    symbolSize: function(val) {
                        return Math.max(val[2] / 50, 8);
                    },
                    showEffectOn: 'render',
                    rippleEffect: {
                        brushType: 'stroke'
                    },
                    hoverAnimation: true,
                    label: {
                        normal: {
                            formatter: '',
                            position: 'right',
                            show: true
                        }
                    },
                    itemStyle: {
                        normal: {
                            color: '#f4e925',
                            shadowBlur: 50,
                            shadowColor: '#EE0000'
                        }
                    },
                    zlevel: 1
                }]
            };
            var myChart = echarts.init(document.getElementById('map'));
            myChart.setOption(option);
        }           
    });
 });




