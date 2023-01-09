var select_provider;

var purchase = {
    details: {
        provider: '',
        total: 0.0,
    },
    addProvider: function (item) {
        this.details.provider = item;
    },
    calculateInvoice: function () {
        var subtotal;
        if ($('input[name="subtotal"]').val() === undefined){
            subtotal = 0.0;
        }else{
            subtotal = $('input[name="subtotal"]').val()
        };
        var total_discount;
        if ($('input[name="total_discount"]').val() === undefined){
            total_discount = 0.0;
        }else{
            total_discount = $('input[name="total_discount"]').val()
        };
        var total_iva;
        if ($('input[name="total_iva"]').val() === undefined){
            total_iva = 0.0;
        }else{
            total_iva = $('input[name="total_iva"]').val()
        };
        this.details.subtotal = parseFloat(subtotal);
        this.details.total_discount = parseFloat(total_discount);
        this.details.total_iva = parseFloat(total_iva);
        this.details.total = this.details.subtotal + this.details.total_iva - this.details.total_discount;
        $('input[name="total"]').val(this.details.total.toFixed(2));
    }
};
    $(function(){
        select_provider = $('#search_provider');

        $('.select2').select2({
            language: 'es',
        });

        select_provider.select2({
            language: 'es',
            allowClear: true,
            placeholder: '',
            minimumInputLength: 1,
            ajax: {
                delay: 250,
                type: 'POST',
                url: pathname,
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: function(params){
                    return{
                        term: params.term,
                        action: 'search_provider'
                    };
                },
                processResults: function(data){
                    return{
                        results:data
                    };
                },
            },
        })
        .on('select2:select', function(e){
            var data = e.params.data;
            if (!Number.isInteger(data.id)) {
                return false;
            }
            purchase.addProvider(data);
        });

        // Form
        $('#add-purchase-form')
            .on('change', 'input[name="subtotal"]', function(){
                purchase.calculateInvoice();
            })
            .on('change', 'input[name="total_discount"]', function(){
                purchase.calculateInvoice();
            })
            .on('change', 'input[name="total_iva"]', function(){
                purchase.calculateInvoice();
            })

        // Inputs $
        $('input[name="subtotal"], input[name="total_discount"], input[name="total_iva"]').TouchSpin({
            verticalbuttons: true,
            verticalupclass: 'glyphicon glyphicon-plus',
            verticaldownclass: 'glyphicon glyphicon-minus',
            initval: 0.00,
            min: 0.00,
            max: 10000000.00,
            step: 1.0,
            decimals: 2,
            prefix: '$',
        })

        // Falta el modal de agregar proveedor

        // Envio de formulario
        $('#add-purchase-form').on('submit', function (e) {
        e.preventDefault();

        var success_url = this.getAttribute('data-url');
        var parameters = new FormData(this);
        parameters.append('provider', JSON.stringify(purchase.details.provider.id));
        parameters.append('total', JSON.stringify(purchase.details.total));
        submit_with_ajax(pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
                    console.log('estoy');
                    location.href = success_url;
                });
    });

    purchase.calculateInvoice();

});
