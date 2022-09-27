// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var events_obseved_pie;
fetch("catalogue.csv")
  .then(response_pie => response_pie.text()) 
  .then(csvString_pie => {
  // Split the csv into rows
  const rows_pie = csvString_pie.split("\n");
  events_obseved_pie = -1 // Skip CSV catalogue header
  for (row_pie of rows_pie) {
    events_obseved_pie = events_obseved_pie + 1
  }

var repeater_parents_pie;
var repeater_children_pie;
fetch("repeaters.json")
  .then(response_rp_pie => response_rp_pie.text()) 
  .then(jsonString_pie => {
  var temp_pie = jsonString_pie;
  count_all = (temp_pie.match(/parent/g) || []).length - 1;
  repeater_parents_pie = (temp_pie.match(/children/g) || []).length - 1;
  repeater_children_pie = (temp_pie.match(/parent":"FRB/g) || []).length;

//console.log('repeater_parents_pie: ');
//console.log(repeater_parents_pie);
//console.log('repeater_children_pie: ');
//console.log(repeater_children_pie+2);
//console.log(events_obseved_pie-(repeater_parents_pie+repeater_children_pie+2));
//console.log(repeater_parents_pie);
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["One-off events", "Repeaters"],
    datasets: [{
      //data: [events_obseved_pie-(repeater_parents_pie+repeater_children_pie), repeater_parents_pie],
      data: [events_obseved_pie-count_all+repeater_parents_pie-repeater_parents_pie, repeater_parents_pie],
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

})

})
