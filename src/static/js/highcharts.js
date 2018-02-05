var chart;

/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
 */
function requestData() {
    $.ajax({
        url: '/live-data',
        success: function(point) {
            var series = chart.series[0],
                shift = series.data.length > 50; // shift if the series is
                                                 // longer than 20

            chart.series[0].addPoint(point, true, shift);
			var gauge = chart2.series[0].points[0],
            newVal = point[1];
            //console.log(newVal)
            chart2.series[0].setData([{y:newVal}]);
            chart2.yAxis[0].update();


            setTimeout(requestData, 8000);
        },
        cache: false
    });
}

function requestData2() {
    $.ajax({
        url: '/live-data',
        success: function(data) {
			 var gauge = chart2.series[0].points[0],
                  newVal = data[1];
                  //console.log(newVal)
                  chart2.series[0].setData([{y:newVal}]);
                  chart2.yAxis[0].update();
            setTimeout(requestData2, 8000);
        },
        cache: false
    });
}


$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container',
            defaultSeriesType: 'areaspline',
            events: {
                load: requestData
            }
        },
        title: {
            text: 'Live Kettle Temperatures'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150,
            maxZoom: 20 * 1000
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Temperature (CELCIUS)',
                margin: 8
            },
            minorGridLineWidth: 0,
            gridLineWidth: 0,
            plotBands: [{ // cold
                from: 15,
                to: 25.5,
                color: 'rgba(68, 170, 213, 0.1)',
                label: {
                    text: 'Cauld as f*ck man',
                    style: {
                        color: '#606060'
                    }
                }
            },
            { // warming
                from: 25.5,
                to: 90.0,
                color: 'rgba(244, 124, 1, 0.1)',
                label: {
                    text: 'It is getting there',
                    style: {
                        color: '#606060'
                    }
                }
            },
					{ // hot
				from: 90.0,
				to: 101.0,
				color: 'rgba(244, 1, 1, 0.1)',
				label: {
					text: 'It is Ready!',
					style: {
						color: '#606060'
					}
				}
			}]
        },
        plotOptions: {
			series: {
				fillColor: {
					linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
					stops: [
						[0, Highcharts.Color('#FF0000').setOpacity(0.4).get('rgba')],
						[1, Highcharts.Color('#0017FF').setOpacity(0.4).get('rgba')]
					]
				}
			}
		},
        series: [{
            name: 'Temperature Point',
            data: [],
            color: '#FF0000'
        }]
    });
    	<!--bar stacked chart start here-->
	chart2 = new Highcharts.Chart({
            chart: {
				renderTo: 'data-container2',
				//events: {
				//	load: requestData2
				//},
				type: 'gauge',
				plotBackgroundColor: null,
				plotBackgroundImage: null,
				plotBorderWidth: 0,
				plotShadow: false
			},

    title: {
        text: 'Temperature Gauge'
    },

    pane: {
        startAngle: -90,
        endAngle: 90,
        background: [{
            backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0, '#FFF'],
                    [1, '#333']
                ]
            },
            borderWidth: 0,
            outerRadius: '109%'
        }, {
            backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0, '#333'],
                    [1, '#FFF']
                ]
            },
            borderWidth: 1,
            outerRadius: '107%'
        }, {
            // default background
        }, {
            backgroundColor: '#DDD',
            borderWidth: 0,
            outerRadius: '105%',
            innerRadius: '103%'
        }]
    },

    // the value axis
    yAxis: {
        min: 0,
        max: 100,

        minorTickInterval: 'auto',
        minorTickWidth: 1,
        minorTickLength: 10,
        minorTickPosition: 'inside',
        minorTickColor: '#666',

        tickPixelInterval: 30,
        tickWidth: 2,
        tickPosition: 'inside',
        tickLength: 10,
        tickColor: '#666',
        labels: {
            step: 2,
            rotation: 'auto'
        },
        title: {
            text: 'degrees C'
        },
        plotBands: [{
            from: 0,
            to: 25,
            color: '#55BF3B' // green
        }, {
            from: 25,
            to: 90,
            color: '#DDDF0D' // yellow
        }, {
            from: 90,
            to: 100,
            color: '#DF5353' // red
        }]
    },

    series: [{
        name: 'Temp',
        data: [],
        tooltip: {
            valueSuffix: ' degrees C'
        }
    }]


});

    <!--bar stacked chart start here-->
});
