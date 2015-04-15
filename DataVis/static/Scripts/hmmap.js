
showHmMapChart()

function showHmMapChart() {
	chart_kind = 'map'
	getData(chart_kind)
	var heatmapInstance = h337.create({
	  container: $('#hmmap_chart')
	})
	heatmapInstance.setData(series_data['series'])
}

function getData(chart_kind){
	$.ajax({
		//url that deal with request and compute
		//async dafault is true, it means that
		//the front will execute the rest script whether there is a return,
		//in this place, async should be false
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
