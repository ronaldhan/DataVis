echarts.util.mapData.params.params.FT = {
    getGeoJson: function (callback) {
        $.getJSON(js_geojson, callback);
    }
} 
var myMapChart = echarts.init(document.getElementById("map_chart"));
var myTimeChart = echarts.init(document.getElementById("time_chart"));

showTimeChart()


function showMapChart() {
	chart_kind = 'map'
	getData(chart_kind);
	var option = getMapOption()
	myMapChart.setOption(option);
};

function showTimeChart() {
	chart_kind = 'time'
	getData(chart_kind);
	option = getTimeOption()
	myTimeChart.setOption(option);
}

//get data from host
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

//get map option
function getMapOption(){
	var option = {
		backgroundColor: '#1b1b1b',
		color: [
			'rgba(255, 255, 255, 0.8)',
			'rgba(14, 241, 242, 0.8)',
			'rgba(37, 140, 249, 0.8)'
		],
		title : {
			text: '微博信息可视化',
			subtext: '丰台地区',
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

function getTimeOption(){
	option = {
		timeline:{
			data:series_data['timeline'],
			label : {
					show: true,
					formatter: null,
					textStyle: {
						color: '#333'
					}
			},
			autoPlay : true,
			playInterval : 1000
		},
		options: make_time_series()
	}
	return option
}

function make_time_series(){
	options = []
	part_options = {
			title : {
				text:'2014-05-01 微博热点区域',
				subtext:'以丰台地区2014年5月份为例'
			},
			toolbox : {
				show:true,
				feature:{
					mark:{show:true},
					dataView:{show:true,readOnly:false},
					restore:{show:true},
					saveAsImage:{show:true}
				}
			},
			dataRange: {
				min: series_data['datarange']['min'],
				max : series_data['datarange']['max'],
				text:['高','低'],           // 文本，默认为数值文本
				calculable : true,
				x: 'left',
				color: ['orangered','yellow','lightskyblue']
			},
			series : [
				{
					name:'timedata',
					type:'map',
					mapType: 'FT',
					data: series_data['series']['2014-05-01']
				}
			]
		}
	options.push(part_options)
	dates = series_data['timeline']
	dcount = dates.length
	sdates = dates.slice(1, dcount)
	option_item = {}

	for (date in sdates){
		data_list = []
		data_dict = {}
		data_dict['data'] = series_data['series'][date]
		data_list.push(data_dict)
		option_item['title'] = {'text': date + ' 微博热点区域'}
		option_item['series'] = data_list
		options.push(option_item)
	}
	return options
}

