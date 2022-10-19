var date_now = new moment().format('YYYY-MM-DD')
var date_range = null;

function report() {
    var parameters = {
    'action': 'search_report',
    'start_date': date_now,
    'end_date': date_now,
}
    if(date_range !== null){
        parameters['start_date'] = date_range.startDate.format('YYYY-MM-DD');
        parameters['end_date'] = date_range.endDate.format('YYYY-MM-DD');
    };

    $('#report').DataTable({
        responsive: true,
        autowidth: false,
        destroy: true,
        deferRender: true,
        order: false,
        paging: false,
        ordering: false,
        fontSize: '1em',
        info: false,
        searching: false,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-primary'
            },
            {
                extend: 'pdfHtml5',
                text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-light',
                download: 'open',
                orientation: 'landscape',
                pageSize: 'LEGAL',
                customize: function (doc) {
                    doc.styles = {
                        header: {
                            fontSize: 18,
                            bold: true,
                            alignment: 'center'
                        },
                        subheader: {
                            fontSize: 13,
                            bold: true
                        },
                        quote: {
                            italics: true
                        },
                        small: {
                            fontSize: 8
                        },
                        tableHeader: {
                            bold: true,
                            fontSize: 11,
                            color: 'white',
                            fillColor: '#2d4154',
                            alignment: 'center'
                        }
                    };
                    doc.content[1].table.widths = ['15%','10%','5%','15%','15%','15%','10%','15%'];
                    doc.content[1].margin = [0, 35, 0, 0];
                    doc.content[1].layout = {};
                    doc['footer'] = (function (page, pages) {
                        return {
                            columns: [
                                {
                                    alignment: 'left',
                                    text: ['Fecha de creación: ', {text: date_now}]
                                },
                                {
                                    alignment: 'right',
                                    text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                }
                            ],
                            margin: 20
                        }
                    });

                }
            }
        ],
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
        columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return  data
                    }
                },
                {
                    targets: [-1, -2, -3, -4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
};

$(function (){
    $('input[name="date_ranger"]').daterangepicker({
      autoUpdateInput: false,
      locale: {
          format: 'YYYY-MM-DD',
          applyLabel: 'Aplicar',
          cancelLabel: 'Cancelar',
      }
  }).on('apply.daterangepicker', function(ev, picker) {
      date_range = picker;
      report();
  }).on('cancel.daterangepicker', function(ev, picker) {
      $(this).data('daterangepicker').setStartDate(date_now);
      $(this).data('daterangepicker').setEndDate(date_now);
      date_range = picker;
      report();
  });
    report();
});
