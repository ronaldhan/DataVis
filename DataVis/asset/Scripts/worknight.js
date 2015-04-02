echarts.util.mapData.params.params.FT = {
    getGeoJson: function (callback) {
        $.getJSON(json_ft, callback);
    }
}

var myWorkNightChart = echarts.init(document.getElementById("worknight_chart"));

showWorkNightChart()

function showWorkNightChart(){
    chart_kind = 'worknight'
	getData(chart_kind);
	var option = getWorkNightOption()
	myWorkNightChart.setOption(option);
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

function getWorkNightOption(){
	var option = {
		backgroundColor: '#1b1b1b',
		color: [
			'rgba(255, 255, 255, 0.8)',
			'rgba(14, 241, 242, 0.8)',
			'rgba(37, 140, 249, 0.8)'
		],
		title : {
			text: '微博信息可视化',
			subtext: '丰台地区--工作日夜晚',
			x:'center',
			textStyle : {
				color: '#fff'
			}
		},
		legend: {
			orient: 'vertical',
			x:'left',
			data:['high', 'middle', 'low'],
			textStyle : {
				color: '#fff'
			}
		},
		dataRange: {
			min: series_data['datarange']['min'],
			max: series_data['datarange']['max'],
			calculable : true,
			color: ['red','yellow','lightgreen'],
			textStyle : {
				color: '#fff'
			}
		},
		toolbox: {
			show : true,
			orient : 'vertical',
			x: 'right',
			y: 'center',
			feature : {
				mark : {show: true},
				dataView : {show: true, readOnly: false},
				restore : {show: true},
				saveAsImage : {show: true}
			}
		},
		series: [
			{
				name: 'low',
				type: 'map',
				mapType: 'FT',
				scaleLimit : {
					max : 2,
					min : 0.8
				},
				itemStyle:{
					normal:{
						borderColor:'rgba(100,149,237,1)',
						borderWidth:0.5,
						areaStyle:{
							color: '#1b1b1b'
						}
					}
				},
				data : [],
				markPoint : {
					symbolSize: 0.5,
					large: true,
					effect : {
						show: false
					},
					data : series_data['series']['low']
				}
			},
			{
				name: 'middle',
				type: 'map',
				mapType: 'FT',
				data : [],
				markPoint : {
					symbolSize: 1.5,
					large: true,
					effect : {
						show: false
					},
					data : series_data['series']['middle']
				}
			},
			{
				name: 'high',
				type: 'map',
				mapType: 'FT',
				hoverable : false,
				data : [],
				markPoint : {
					symbol : 'diamond',
					symbolSize: 5,
					large: true,
					effect : {
						show: true
					},
					data : series_data['series']['high']
				}
			}
		]
	}
	return option
}