var mySevenLineChart = echarts.init(document.getElementById("seven_line_chart"));
var myTwoLineChart = echarts.init(document.getElementById("two_line_chart"));

showLineChart()

function showLineChart() {
	chart_kind = 'line'
	getData(chart_kind);
	optionSeven = getSevenLineOption()
	optionTwo = getTwoLineOption()
	mySevenLineChart.setOption(optionSeven);
	myTwoLineChart.setOption(optionTwo);
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

function getSevenLineOption(){
    var option = {
        tooltip : {
            show: true,
            trigger: 'item'
        },
        legend: {
            data:['周一','周二','周三','周四','周五','周六','周日']
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
        series : [
            {
                name:'周一',
                type:'line',
                data:series_data['series']['t1'],
                markPoint : {
                    data : [
                        {type : 'max', name: '最大值'},
                        {type : 'min', name: '最小值'}
                    ]
                }
            },
            {
                name:'周二',
                type:'line',
                data:series_data['series']['t2'],
                markPoint : {
                    data : [
                        {type : 'max', name: '最大值'},
                        {type : 'min', name: '最小值'}
                    ]
                }
            },
            {
                name:'周三',
                type:'line',
                data:series_data['series']['t3'],
                markPoint : {
                    data : [
                        {type : 'max', name: '最大值'},
                        {type : 'min', name: '最小值'}
                    ]
                }
            },
            {
                name:'周四',
                type:'line',
                data:series_data['series']['t4'],
                markPoint : {
                    data : [
                        {type : 'max', name: '最大值'},
                        {type : 'min', name: '最小值'}
                    ]
                }
            },
            {
                name:'周五',
                type:'line',
                data:series_data['series']['t5'],
                markPoint : {
                    data : [
                        {type : 'max', name: '最大值'},
                        {type : 'min', name: '最小值'}
                    ]
                }
            },
            {
                name:'周六',
                type:'line',
                data:series_data['series']['t6'],
                markPoint : {
                    data : [
                        {type : 'max', name: '最大值'},
                        {type : 'min', name: '最小值'}
                    ]
                }
            },
            {
                name:'周日',
                type:'line',
                data:series_data['series']['t7'],
                markPoint : {
                    data : [
                        {type : 'max', name: '最大值'},
                        {type : 'min', name: '最小值'}
                    ]
                }
            }
        ]
    }
    return option
}

function getTwoLineOption(){
    var option = {
        tooltip : {
            show: true,
            trigger: 'item'
        },
        legend: {
            data:['工作日','周末']
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
        series : [
            {
                name:'工作日',
                type:'line',
                data:series_data['series']['workday'],
                markPoint : {
                    data : [
                        {type : 'max', name: '最大值'},
                        {type : 'min', name: '最小值'}
                    ]
                }
            },
            {
                name:'周末',
                type:'line',
                data:series_data['series']['weekend'],
                markPoint : {
                    data : [
                        {type : 'max', name: '最大值'},
                        {type : 'min', name: '最小值'}
                    ]
                }
            }
        ]
    }
    return option
}

