document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript is loaded!');
});

google.charts.load('current', {'packages':['corechart', 'line']});
google.charts.setOnLoadCallback(drawChart);

// URL of your REST API
const apiUrl = 'https://web-country-list-zytwh45bcq-uc.a.run.app/gdppc'; 

// Function to fetch data from the API
async function fetchData() {
    try {
        console.log(apiUrl);
        const response = await fetch(apiUrl);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Function to draw the chart
async function drawChart() {
    const data = await fetchData();

    // Create a DataTable
    const dataTable = new google.visualization.DataTable();
    dataTable.addColumn('datetime', 'date');
    dataTable.addColumn('number', 'gdppc');

    console.log(dataTable);
    // Format data for Google Charts
    const formattedData = data.map(entry => [new Date(entry.time), entry.value]);

    // Add rows to the DataTable
    dataTable.addRows(formattedData);

    // Set chart options
    const options = {
        title: 'Time Series Data',
        hAxis: { title: 'Time' },
        vAxis: { title: 'Value' },
        legend: { position: 'none' }
    };

    // Create and draw the chart
    const chart = new google.visualization.LineChart(document.getElementById('myChart'));
    chart.draw(dataTable, options);
}