echarts.util.mapData.params.params.FT = {
    getGeoJson: function (callback) {
        $.getJSON(js_geojson, callback);
    }
} 
var myChart = echarts.init(document.getElementById("main"));

refresh()


function refresh() {
	getMapData();
	var option = getMapOption()
	myChart.setOption(option);
};
//get map data from host
function getMapData(){
	$.ajax({
		//url that deal with request and compute
		//async dafault is true, it means that
		//the front will execute the rest script whether there is a return,
		//in this place, async should be false
		url: "/weibovis/getdata/",
		data: { kind: 'map'},
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
		backgroundColor: '#D3D3D3',
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
			data:['check-count'],
			textStyle : {
				color: '#fff'
			}
		},
		dataRange: {
			min: series_data['datarange']['min'],
			max: series_data['datarange']['max'],
			calculable : true,
			color: ['maroon','purple','red','orange','yellow','lightgreen']
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
				name: 'check-count',
				type: 'map',
				mapType: 'FT',
				itemStyle:{
					normal:{
						borderColor:'rgba(100,149,237,1)',
						borderWidth:1.5,
						areaStyle:{
							color: '#1b1b1b'
						}
					}
				},
				data : [],
				markPoint : {
					symbolSize: 2,
					large: true,
					effect : {
						show: true
					},
					data : series_data['series']
				}
			}
		]
	}
	return option
}

