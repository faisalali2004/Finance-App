// static/js/charts.js

document.addEventListener('DOMContentLoaded', () => {
    // This file will contain the Chart.js initialization logic
    // for your pie chart and line chart on the dashboard.
    //
    // Example structure for chart initialization (will be expanded later):
    //
    // function renderPieChart(data, labels) {
    //     const ctx = document.getElementById('pieChart').getContext('2d');
    //     new Chart(ctx, {
    //         type: 'pie',
    //         data: {
    //             labels: labels,
    //             datasets: [{
    //                 data: data,
    //                 backgroundColor: [
    //                     'rgba(255, 99, 132, 0.8)',
    //                     'rgba(54, 162, 235, 0.8)',
    //                     'rgba(255, 206, 86, 0.8)',
    //                     'rgba(75, 192, 192, 0.8)',
    //                     'rgba(153, 102, 255, 0.8)'
    //                 ],
    //             }]
    //         },
    //         options: {
    //             responsive: true,
    //             plugins: {
    //                 legend: {
    //                     position: 'top',
    //                     labels: {
    //                         color: 'rgb(107 114 128)' // gray-600 for light mode
    //                     }
    //                 },
    //                 tooltip: {
    //                     callbacks: {
    //                         label: function(context) {
    //                             let label = context.label || '';
    //                             if (label) {
    //                                 label += ': ';
    //                             }
    //                             if (context.parsed !== null) {
    //                                 label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'PKR' }).format(context.parsed);
    //                             }
    //                             return label;
    //                         }
    //                     }
    //                 }
    //             }
    //         }
    //     });
    // }
    //
    // function renderLineChart(data, labels) {
    //     const ctx = document.getElementById('lineChart').getContext('2d');
    //     new Chart(ctx, {
    //         type: 'line',
    //         data: {
    //             labels: labels,
    //             datasets: [{
    //                 label: 'Spending Trend',
    //                 data: data,
    //                 borderColor: 'rgba(59, 130, 246, 1)', // blue-500
    //                 backgroundColor: 'rgba(59, 130, 246, 0.2)',
    //                 tension: 0.1,
    //                 fill: true
    //             }]
    //         },
    //         options: {
    //             responsive: true,
    //             plugins: {
    //                 legend: {
    //                     position: 'top',
    //                     labels: {
    //                         color: 'rgb(107 114 128)' // gray-600 for light mode
    //                     }
    //                 }
    //             },
    //             scales: {
    //                 x: {
    //                     ticks: {
    //                         color: 'rgb(107 114 128)'
    //                     },
    //                     grid: {
    //                         color: 'rgba(229, 231, 235, 0.3)'
    //                     }
    //                 },
    //                 y: {
    //                     ticks: {
    //                         color: 'rgb(107 114 128)'
    //                     },
    //                     grid: {
    //                         color: 'rgba(229, 231, 235, 0.3)'
    //                     }
    //                 }
    //             }
    //         }
    //     });
    // }
    //
    // You would call these functions from your dashboard template (index.html)
    // after fetching data, or pass data directly to them.
});
