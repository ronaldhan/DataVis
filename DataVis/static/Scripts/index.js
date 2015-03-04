var pathname = location.pathname;
var pathlevel = pathname.slice(0, pathname.indexOf('index'));

echarts.util.mapData.params.params.FT = {
    getGeoJson: function (callback) {
        $.getJSON(pathlevel + 'geoJson/FT.json', callback);
    }
} 
var myChart = echarts.init(document.getElementById("main"));
var placeList = [
	{ name: '美高美', geoCoord: [116.090316745, 39.8066538017] },
	{ name: '南宫饭店', geoCoord: [116.14783293, 39.8037860467] },
	{ name: '淮阳村', geoCoord: [116.168974437, 39.8040199854] },
	{ name: '翠云山庄', geoCoord: [116.154235095, 39.8162342218] },
	{ name: '北方宾馆', geoCoord: [116.180089174, 39.8079383742] },
	{ name: '京西南宫宾馆', geoCoord: [116.148811202, 39.8080363974] }
]
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
		data:['强','中','弱'],
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
		    name: '弱',
		    type: 'map',
		    mapType: 'FT',
		    itemStyle: {
			    normal: {
				    borderColor: 'rgba(100,149,237,1)',
				    borderWidth: 1.5,
				    areaStyle: {
					    color: '#1b1b1b'
				    }
			    }
		    },
		    data: [],
		    markPoint: {
			    symbolSize: 2,
			    large: true,
			    effect: {
				    show: true
			    },
			    data: (function () {
				    var data = [];
				    var len = 2;
				    var geoCoord
				    while (len--) {
					    geoCoord = placeList[len % placeList.length].geoCoord;
					    data.push({
					        name: placeList[len % placeList.length].name + len,
					        value: 10,
					        geoCoord: [
					            geoCoord[0] + Math.random() * 5 * -1,
					            geoCoord[1] + Math.random() * 3 * -1
					        ]
					    })
				    }
				    return data;
			    })()
		    }
	    },
	    {
		    name: '中',
		    type: 'map',
		    mapType: 'FT',
		    data: [],
		    markPoint: {
			    symbolSize: 3,
			    large: true,
			    effect: {
				    show: true
			    },
			    data: (function () {
				    var data = [];
				    var len = 2;
				    var geoCoord
				    while (len--) {
					    geoCoord = placeList[(len + 3) % placeList.length].geoCoord;
					    data.push({
					        name: placeList[(len + 3) % placeList.length].name + len,
					        value: 50,
					        geoCoord: [
					            geoCoord[0] + Math.random() * 5 * -1,
					            geoCoord[1] + Math.random() * 3 * -1
					        ]
					    })
				    }
				    return data;
			    })()
		    }
	    },
	    {
		    name: '强',
		    type: 'map',
		    mapType: 'FT',
		    hoverable: false,
		    roam: true,
		    data: [],
		    markPoint: {
			    symbol: 'diamond',
			    symbolSize: 6,
			    large: true,
			    effect: {
				    show: true
			    },
			    data: (function () {
				    var data = [];
				    var len = placeList.length;
				    while (len--) {
					    data.push({
					        name: placeList[len].name,
					        value: 90,
					        geoCoord: placeList[len].geoCoord
					    })
				    }
				    return data;
			    })()
		    }
	    }
    ]
};
myChart.setOption(option);
