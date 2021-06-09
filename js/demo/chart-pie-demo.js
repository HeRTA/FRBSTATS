// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var events_obseved;
fetch("../../catalogue.csv")
  .then(response => response.text()) 
  .then(csvString => {
  // Split the csv into rows
  const rows = csvString.split("\n");
  events_obseved = -1 // Skip CSV catalogue header
  for (row of rows) {
    events_obseved = events_obseved + 1
  }
});
var repeater_parents;
var repeater_children;
fetch("../../repeaters.json")
  .then(response => response.text()) 
  .then(jsonString => {
  var temp = jsonString;
  repeater_parents = (temp.match(/children/g) || []).length - 1;
  repeater_children = (temp.match(/parent":"FRB/g) || []).length - 1;
});

var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["One-off events", "Repeaters"],
    datasets: [{
      data: [events_obseved-(repeater_parents+repeater_children), repeater_parents],
      backgroundColor: ['#4e73df', '#1cc88a'],
      hoverBackgroundColor: ['#2e59d9', '#17a673'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});
