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