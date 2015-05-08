showPathMapChart()


function showPathMapChart(){
	chart_kind = 'path'
	getData(chart_kind)
	var map = new BMap.Map("path_chart")
	//ft district
	map.centerAndZoom(new BMap.Point(116.293, 39.846), 12)
	map.addControl(new BMap.MapTypeControl());
	map.setCurrentCity("北京");
	map.enableScrollWheelZoom(true);
	var top_left_control = new BMap.ScaleControl({anchor: BMAP_ANCHOR_TOP_LEFT});
	var top_left_navigation = new BMap.NavigationControl();
	map.addControl(top_left_control);
	map.addControl(top_left_navigation);

	// use the data to construct line in map
	user_points = series_data['series']
	// for in this place the user get the keys in dict
	for (user in user_points) {
		points = user_points[user]
		var path = []
		for (point in points) {
			path.append(new BMap.Point(point[0], point[1]))
		}
		var polyline = new BMap.Polyline(path, {strokeColor:"blue", strokeWeight:2, strokeOpacity:0.5});
		map.addOverlayer(polyline)
	}
}

function getData(chart_kind){
	$.ajax({
		url: "/weibovis/getpathdata/",
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
