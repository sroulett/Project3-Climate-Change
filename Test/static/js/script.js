

let line_chart_data = "http://127.0.0.1:5000/api/temperature_data"
function init() {
d3.json(line_chart_data).then((data) => {

// Extract unique countries
const uniqueCountries = [...new Set(data.map(item => item.Country))];

console.log(uniqueCountries);

 // Use d3 to select the dropdown with id of `#selDataset`
 let selector = d3.select("#countryDropdown");

 // Use the list of sample names to populate the select options
 // Hint: Inside a loop, you will need to use d3 to append a new
 // option for each sample name.
 uniqueCountries.forEach((sample) => {
   selector
       .append("option")
       .text(sample)
       .property("value", sample);
});
let first_sample = uniqueCountries[0]

    // Build charts and metadata panel with the first sample
    buildCharts(first_sample)
});
}

// Function for event listener
function optionChanged(newSample) {
    // Build charts and metadata panel each time a new sample is selected
    buildCharts(newSample)

  }
  function buildCharts(sample) {
    d3.json(line_chart_data).then((data) => {
  
  
      // Filter the samples for the object with the desired sample number
      let filterdata = data.filter( x => x.Country == sample)

console.log(filterdata)


// Create lists for average temperatures and decades
const averageTemperatures = filterdata.map(item => item.AverageTemperature);
const decades = filterdata.map(item => item.Decade);

console.log("Average Temperatures:", averageTemperatures);
console.log("Decades:", decades);


const trace = [{
    x: decades,
    y: averageTemperatures,
    mode: 'lines+markers',
    type: 'scatter',
    marker: { color: 'blue' },
    line: { shape: 'linear' },
}];


const layout = {
    title: 'Average Temperatures Over Decades',
    xaxis: {
        title: 'Decades',
        showgrid: true,
    },
    yaxis: {
        title: 'Average Temperature (°C)',
        showgrid: true,
    },
};

Plotly.newPlot('lineChart', trace, layout);
  

    })}      
init()