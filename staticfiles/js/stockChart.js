
var symbol = 'NABIL'

Highcharts.getJSON('https://www.sharesansar.com/company-chart/history?symbol='+symbol+'&resolution=1D&from=1514764800&to=1645548668', function (data) {
    ohlc =[]
    for(var i = 0; i<data.t.length; i++){
        var date = data['t'][i]*1000;
        var open = data['o'][i];
        var high = data['h'][i];
        var low = data['l'][i];
        var close = data['c'][i];
        ohlc.push([date,parseFloat(open),parseFloat(high),parseFloat(low),parseFloat(close)])       
    }

    Highcharts.stockChart('container', {


        rangeSelector: {
            selected: 1
        },
        navigator: {
            series: {
                color: Highcharts.getOptions().colors[0]
            }
        },

        title: {
            text: symbol+' Stock Price'
        },

        series: [{
            type: 'hollowcandlestick',
            name: symbol+' Stock Price',
            data: ohlc,
            dataGrouping: {
                units: [
                    [
                        'week', // unit name
                        [1] // allowed multiples
                    ], [
                        'month',
                        [1, 2, 3, 4, 6]
                    ]
                ]
            }
        }]
    });
});



