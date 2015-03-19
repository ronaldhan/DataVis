var myBarChart = echarts.init(document.getElementById("bar_chart"));

showBarChart()

function showBarChart() {
	chart_kind = 'bar'
	getData(chart_kind);
	option = getBarOption()
	myBarChart.setOption(option);
}


function getData(chart_kind){
	$.ajax({
		//url that deal with request and compute
		//async dafault is true, it means that
		//the front will execute the rest script whether there is a return,
		//in this place, async should be false
		url: "/weibovis/getdata/",
		data: { kind: chart_kind},
		cache: false,
		async: false,
		dataType: "json",
		success: function (data) {
			if (data != null) {
				if (data) {
					//get the data now
					console.log('get data success')
					series_data = data
				}
			}
		},
		error: function (e) {
			console.log('get data error from the host')
		}
	});
};


function getBarOption(){
    var option = {
        tooltip : {
            show: true,
            trigger: 'item'
        },
        legend: {
            data:['白天','夜晚','总计']
        },
        toolbox: {
            show : true,
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                data : series_data['series']['xaxis']
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
        series :[
            {
                name:'白天',
                type:'bar',
                itemStyle: {        // 系列级个性化样式，纵向渐变填充
                    normal: {
                        barBorderColor:'red',
                        barBorderWidth: 2,
                        color : #FF6600
                    },
                    emphasis: {
                        barBorderWidth: 2,
                        barBorderColor:'green',
                        color: (function (){
                            var zrColor = require('zrender/tool/color');
                            return zrColor.getLinearGradient(
                                0, 400, 0, 300,
                                [[0, 'red'],[1, 'orange']]
                            )
                        })(),
                        label : {
                            show : true,
                            position : 'top',
                            formatter : "{a} {b} {c}",
                            textStyle : {
                                color: 'blue'
                            }
                        }
                    }
                },
                data:series_data['series']['day']
            },
            {
                name:'夜晚',
                type:'bar',
                itemStyle: {                // 系列级个性化
                    normal: {
                        barBorderWidth: 2,
                        barBorderColor:'tomato',
                        color: '#00CCCC'
                    },
                    emphasis: {
                        barBorderColor:'red',
                        color: 'blue'
                    }
                },
                data:series_data['series']['night']
            },
            {
                name:'总计',
                type:'bar',
                itemStyle: {
                    normal: {                   // 系列级个性化，横向渐变填充
                        borderRadius: 2,
                        color : (function (){
                            var zrColor = require('zrender/tool/color');
                            return zrColor.getLinearGradient(
                                0, 0, 1000, 0,
                                [[0, 'rgba(30,144,255,0.8)'],[1, 'rgba(138,43,226,0.8)']]
                            )
                        })(),
                        label : {
                            show : true,
                            textStyle : {
                                fontSize : '16',
                                fontFamily : '微软雅黑',
                                fontWeight : 'bold'
                            }
                        }
                    }
                },
                data: series_data['series']['total'],
                markLine : {
                    data : [
                        {type : 'average', name : '平均值'},
                        {type : 'max'},
                        {type : 'min'}
                    ]
                }
            }
        ]
    }
    return option
};