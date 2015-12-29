echarts.util.mapData.params.params.GRID = {
    getGeoJson: function (callback) {
        $.getJSON(json_grid, callback);
    }
}

var myTimeChart = echarts.init(document.getElementById("time_chart"));

showTimeChart()

function showTimeChart() {
	chart_kind = 'time'
	getData(chart_kind);
	option = getTimeOption()
	myTimeChart.setOption(option);
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

function getTimeOption(){
	option = {
		backgroundColor: '#1b1b1b',
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
			playInterval : 2000
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
				max : 50,
				text:['高','低'],           // 文本，默认为数值文本series_data['datarange']['max']
				calculable : true,
				x: 'left',
				color: ['orangered','yellow','lightskyblue']
			},
			series : [
				{
					name:'timedata',
					type:'map',
					mapType: 'GRID',
					data: series_data['series']['2014-05-01']
				}
			]
		}
	options.push(part_options)
	dates = series_data['timeline']
	dcount = dates.length
	sdates = dates.slice(1, dcount)


	for (var i=0;i<sdates.length;i++){
		option_item = {}
		data_list = []
		data_dict = {}
		data_dict['data'] = series_data['series'][sdates[i]]
		data_list.push(data_dict)
		option_item['title'] = {'text': sdates[i] + ' 微博热点区域'}
		option_item['series'] = data_list
		options.push(option_item)
	}
	return options
}
