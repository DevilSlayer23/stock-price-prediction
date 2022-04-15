 const ctx = document.getElementById('myCanvas').getContext('2d');


    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Cases',
                data: CaseData,
                backgroundColor: [
                    'Blue',
                ],
                borderColor: 'blue',
                borderAlign : 'inner',
                borderWidth : "0.1",
                fill: false,
                cubicInterpolationMode: 'monotone',
                tension: 0.4,
            },
        ]
        },
        options: {
            responsive: true,
            elements: {

                line: {
                    tension: 0, // disables bezier curves
                }
            },
            scales: {
                x:{
                    offset : false,
                    type : "time",
                    time : {
                        unit : "month",
                    },
                    grid : {
                        offset : false,
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });