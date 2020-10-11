  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);
  
  function drawChart() {

    var data = google.visualization.arrayToDataTable([
      ['Priority Level', '# of tickets'],
      ['Critical', 2],
      ['High',     8],
      ['Medium',      3],
      ['Low',  11],
    ]);

    var options = {
      title: '',
      is3D: true,
    };

    var chart = new google.visualization.PieChart(document.getElementById('piechart'));

    chart.draw(data, options);
  }