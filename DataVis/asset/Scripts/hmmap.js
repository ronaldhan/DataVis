
showHmMapChart()

function showHmMapChart() {
	chart_kind = 'map'
	getData(chart_kind)
	var heatmapInstance = h337.create({
	  container: document.getElementById('hmmap_chart'),
	})
	var heat = simpleheat(hmmap_chart)
	var series = series_data['series']
	var data = series['data']
	var points = []
	var max = series['max']
	var min = series['min']
	for (var i=0;i<data.length;i++) {
		var point = {
			x: data[i]['x'],
			y: data[i]['y'],
			value: data[i]['value'],
		}
		points.push(point)
	}
	var d = { max: max, min: min, data: points }
	heatmapInstance.setData(d)
}

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
