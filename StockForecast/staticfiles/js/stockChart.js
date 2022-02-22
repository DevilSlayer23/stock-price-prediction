
let symbol = {{ symbol | safe}};
let startDate = Math.floor(new Date('2021.01.01').getTime() / 1000);
let endDate = Math.floor(new Date().getTime() / 1000)
console.log(startDate)

// window.onload = function () {
//     var dataPoints1 = [], dataPoints2 = [];
//     var stockChart = new CanvasJS.StockChart("chartContainer", {
//         theme: "light2",
//         exportEnabled: true,
//         title: {
//             text: ""
//         },
//         charts: [{
//             axisY: {
//                 prefix: "$"
//             },
//             data: [{
//                 type: "candlestick",
//                 yValueFormatString: "#,###.00",
//                 dataPoints: dataPoints1
//             }]
//         }],
//         navigator: {
//             data: [{
//                 color: "#6D78AD",
//                 dataPoints: dataPoints2
//             }],
//             slider: {
//                 minimum: new Date(2021, 01, 01),
//                 maximum: new Date()
//             }
//         }
//     });
     
//     function getData() {
//         const url = "https://www.sharesansar.com/company-chart/history?symbol=" + symbol + "&resolution=1D&from=" + startDate + "to=" + endDate;
         
//             //      turnover = data.turnover;
   
//             console.log(data.t[0])
//             for (var i = 0; i < data.t.length; i++) {
//                 date = new Date(data.t[i] * 1000)
//                 high = data.h[i];
//                 low = data.l[i];
//                 open = data.o[i];
//                 close = data.c[i];
//                 console.log(high)
//                 dataPoints1.push({ x: date, y: [Number(high), Number(low), Number(open), Number(close)] });
//                 dataPoints2.push({ x: date, y: close });
//             }
//             stockChart.render();
//         });
//     }
// }

const url = "https://www.sharesansar.com/company-chart/history?symbol=NABIL";

/**
 * Load new data depending on the selected min and max
 */
function afterSetExtremes(e) {
  
    const { chart } = e.target;
    chart.showLoading('Loading data from server...');
    fetch(`${url}&from=${new Date(Math.round(e.min))}&to=${new Date(Math.round(e.max))}`)
        .then(res => res.ok && res.json())
        .then(data => {
            console.log(data)
            chart.series[0].setData(data['t']);
            chart.hideLoading();
        }).catch(error => console.error(error.message));
}

fetch(url)
    .then(res => res.ok && res.json())
    .then(data => {

        // Add a null value for the end date
        data.push([Date.UTC(2011, 9, 14, 18), null, null, null, null]);

        // create the chart
        Highcharts.stockChart('chartContainer', {
            chart: {
                type: 'candlestick',
                zoomType: 'x'
            },

            navigator: {
                adaptToUpdatedData: false,
                series: {
                    data: data
                }
            },

            scrollbar: {
                liveRedraw: false
            },

            title: {
                text: 'AAPL history by the minute from 1998 to 2011',
                align: 'left'
            },

            subtitle: {
                text: 'Displaying 1.7 million data points in Highcharts Stock by async server loading',
                align: 'left'
            },

            rangeSelector: {
                buttons: [{
                    type: 'hour',
                    count: 1,
                    text: '1h'
                }, {
                    type: 'day',
                    count: 1,
                    text: '1d'
                }, {
                    type: 'month',
                    count: 1,
                    text: '1m'
                }, {
                    type: 'year',
                    count: 1,
                    text: '1y'
                }, {
                    type: 'all',
                    text: 'All'
                }],
                inputEnabled: false, // it supports only days
                selected: 4 // all
            },

            xAxis: {
                events: {
                    afterSetExtremes: afterSetExtremes
                },
                minRange: 3600 * 1000 // one hour
            },

            yAxis: {
                floor: 0
            },

            series: [{
                data: data,
                dataGrouping: {
                    enabled: false
                }
            }]
        });
    }).catch(error => console.error(error.message));