google.charts.load('current', {'packages':['corechart']});
google.charts.load('current', {'packages':['gauge']});
google.charts.setOnLoadCallback(drawPriorityLevel);
google.charts.setOnLoadCallback(drawSLAViolations);
google.charts.setOnLoadCallback(drawByWeek);
google.charts.setOnLoadCallback(drawTicketBreakdown);


// PRIORITY LEVEL CHART - PIE
function drawPriorityLevel() {

	var data = google.visualization.arrayToDataTable([
	  ['Priority Level', 'Number of Open Tickets'],
	  ['P1', 11],
	  ['P2', 2],
	  ['P3', 2],
	  ['P4', 2],
	  ['P5', 7]
	]);

	var options = {
	  width: 300, height: 300,
	  legend: 'none',
	  colors: ['#e0440e', '#e6693e', '#ec8f6e', '#f3b49f', '#f6c7b6']
	};

	var chart = new google.visualization.PieChart(document.getElementById('priority_chart'));

	chart.draw(data, options);
}


// SLA VIOLATIONS CHART - GAUGE
function drawSLAViolations() {

	var data = google.visualization.arrayToDataTable([
	  ['Label', 'Value'],
	  ['Overdue', 3]
	]);

	var options = {
	  width: 215, height: 215,
	  yellowFrom: 5, yellowTo: 10,
	  redFrom: 10, redTo: 15,
	  minorTicks: 1, max: 15
	};

	var chart = new google.visualization.Gauge(document.getElementById('violations_chart'));

	chart.draw(data, options);
}

// ISSUES THIS WEEK - LINE
function drawByWeek() {
	var data = google.visualization.arrayToDataTable([
	  ['Day', 'Opened Issues', 'Closed Issues'],
	  ['Monday',  10, 3],
	  ['Tuesday',  7, 9],
	  ['Wednesday',  6, 1],
	  ['Thursday',  10, 4],
	  ['Friday', 3, 7]
	]);

	var options = {
	  curveType: 'none',
	  legend: { position: 'bottom' },
	  width: 600, height: 300
	};

	var chart = new google.visualization.LineChart(document.getElementById('by_week_chart'));

	chart.draw(data, options);
}

// CURRENT ISSUE BREAKDOWN - COLUMN BAR
function drawTicketBreakdown() {
  var data = google.visualization.arrayToDataTable([
	["Ticket Status", "Ticket Type"],
	["Open", 8],
	["Closed", 10],
	["Overdue", 1]
  ]);

  var options = {
	width: 500,
	height: 300,
	legend: 'none',
/* 	bar: {groupWidth: "95%"}, */
  };
  
  var chart = new google.visualization.ColumnChart(document.getElementById("breakdown_chart"));
  
  chart.draw(data, options);
}