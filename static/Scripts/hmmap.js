showHmMapChart()

//function setGradient(){
//	/*格式如下所示:
//	{
//		0:'rgb(102, 255, 0)',
//		.5:'rgb(255, 170, 0)',
//		1:'rgb(255, 0, 0)'
//	}*/
//	var gradient = {};
//	var colors = document.querySelectorAll("input[type='color']");
//	colors = [].slice.call(colors,0);
//	colors.forEach(function(ele){
//		gradient[ele.getAttribute("data-key")] = ele.value;
//	});
//	heatmapOverlay.setOptions({"gradient":gradient});
//}

function showHmMapChart(){
	chart_kind = 'map'
	getData(chart_kind)
	var map = new BMap.Map("hmmap_chart")
	//ft district
	map.centerAndZoom(new BMap.Point(116.293, 39.846), 12)
	map.addControl(new BMap.MapTypeControl());
	map.setCurrentCity("北京");
	map.enableScrollWheelZoom(true);
	var top_left_control = new BMap.ScaleControl({anchor: BMAP_ANCHOR_TOP_LEFT});
	var top_left_navigation = new BMap.NavigationControl();
	map.addControl(top_left_control);
	map.addControl(top_left_navigation);
	heatmapOverlay = new BMapLib.HeatmapOverlay({"radius":30});
	map.addOverlay(heatmapOverlay);
	heatmapOverlay.setDataSet(series_data['series'])
	var gradient = {
		.2:'Blue',
		.4:'cyan',
		.6:'Yellow',
		.8:'Red',
		1:'White'
	}
	heatmapOverlay.setOptions({"gradient":gradient})
	heatmapOverlay.show();
}
//function showHmMapChart() {
//	chart_kind = 'map'
//	getData(chart_kind)
//	var heatmapInstance = h337.create({
//	  container: document.getElementById('hmmap_chart'),
//	})
//	var heat = simpleheat(hmmap_chart)
//	var series = series_data['series']
//	var data = series['data']
//	var points = []
//	var max = series['max']
//	var min = series['min']
//	for (var i=0;i<data.length;i++) {
//		var point = {
//			x: data[i]['x'],
//			y: data[i]['y'],
//			value: data[i]['value'],
//		}
//		points.push(point)
//	}
//	var d = { max: max, min: min, data: points }
//	heatmapInstance.setData(d)
//}

function getData(chart_kind){
	$.ajax({
		url: "/weibovis/getheatmapdata/",
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
