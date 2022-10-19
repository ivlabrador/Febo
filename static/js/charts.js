$(document).ready(function(){

    var ctx = $('#sales-chart');

    var labels = [
          'Enero',
          'Febrero',
          'Marzo',
          'Abril',
          'Mayo',
          'Junio',
          'Julio',
          'Agosto',
          'Septiembre',
          'Octubre',
          'Noviembre',
          'Diciembre',
        ];
    var data = {
          labels: labels,
          datasets: [{
            label: 'Ventas Año {{year}}',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [0, 10, 5, 2, 20, 30, 45],
          }]
        };
    var options = {}

    var myChart = new Chart(ctx, {
      type: 'line',
      data: data,
      options: options,
    });
})
