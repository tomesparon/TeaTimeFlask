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
                shift = series.data.length > 20; // shift if the series is
                                                 // longer than 20

            // add the point
            chart.series[0].addPoint(point, true, shift);

            // call it again after nine seconds
            setTimeout(requestData, 9000);
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
                from: 20,
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
                to: 70.5,
                color: 'rgba(244, 124, 1, 0.1)',
                label: {
                    text: 'It is getting there',
                    style: {
                        color: '#606060'
                    }
                }
            },
					{ // hot
				from: 70.5,
				to: 80.5,
				color: 'rgba(244, 1, 1, 0.1)',
				label: {
					text: 'It is DONE',
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
});
