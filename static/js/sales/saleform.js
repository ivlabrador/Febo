var dataSale;
var select_client, select_search_product;
var tblSearchProducts;

var sale = {
    details: {
        client: '',
        subtotal: 0.0,
        total_discount: 0.0,
        total_iva: 0.0,
        total: 0.0,
        products: [],
    },
    addClient: function (item) {
        this.details.client = item;
    },
    getProductsIds: function () {
        return this.details.products.map(value => value.id);
    },
    calculateInvoice: function () {
        var price;
        if ($('input[name="price"]').val() === undefined){
            price = 0.0;
        }else{
            price = $('input[name="price"]').val()
        };
        var quantity;
        if ($('input[name="quantity"]').val() === undefined){
            quantity = 1;
        }else{
            quantity = $('input[name="quantity"]').val()
        };
        var discount;
        if ($('input[name="discount"]').val() === undefined){
            discount = 0.0;
        }else{
            discount = $('input[name="discount"]').val();
        };
        var subtotal = 0.0;
        var total_iva = 0.0;
        var total_discount = 0.0;
        this.details.products.forEach(function (value, index, array) {
            value.index = index;
            value.quantity = parseInt(value.quantity);
            value.price = parseFloat(value.price);
            value.discount = parseFloat(value.discount);
            value.iva = parseFloat(value.iva);
            value.subtotal = value.quantity * value.price;
            if(value.discount != 0.0){
                total_discount += (value.subtotal/100) * value.discount;
                console.log(total_discount);
            }else{
                total_discount += 0.0;
            }
            total_iva += (value.subtotal/100) * value.iva;
            subtotal += value.subtotal;
        });
        this.details.subtotal = subtotal;
        this.details.total_iva = total_iva;
        this.details.total_discount = total_discount;
        this.details.total = this.details.subtotal + this.details.total_iva - this.details.total_discount;
        $('input[name="subtotal"]').val(this.details.subtotal.toFixed(2));
        $('input[name="total_iva"]').val(this.details.total_iva.toFixed(2));
        $('input[name="total_discount"]').val(this.details.total_discount.toFixed(2));
        $('input[name="total"]').val(this.details.total.toFixed(2));
    },
    addProduct: function (item) {
        this.details.products.push(item);
        this.listProducts();
        console.log(item);
    },
    listProducts: function () {
        this.calculateInvoice();
        dataSale = $('#dataSale').DataTable({
            responsive: true,
            autoWidth: true,
            destroy: true,
            data: this.details.products,
            columns: [
                {"data": "id"},
                {"data": "name"},
                {"data": "stock"},
                {"data": "price"},
                {"data": "quantity"},
                {"data": "discount"},
                {"data": "iva"},
                {"data": "subtotal"}
            ],
            columnDefs: [
                {
                    targets: [-6],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.is_active) {
                            return '<span>Sin stock</span>';
                        }
                        return '<span>' + parseInt(data) + '</span>';
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn"><i class="fa-solid fa-trash-can"></i></a>';
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="price" class="form-control-sm input-sm" autocomplete="off" value="' + row.price + '">';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="quantity" class="form-control-sm input-sm" autocomplete="off" value="' + row.quantity + '">';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="discount" class="form-control-sm input-sm" autocomplete="off" value="' + row.discount + '">';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '%' + parseInt(data);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                }

            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                $(row).find('input[name="quantity"]').TouchSpin({
                    verticalbuttons: true,
                    verticalupclass: 'glyphicon glyphicon-plus',
                    verticaldownclass: 'glyphicon glyphicon-minus',
                    min: 1,
                    max: parseInt(data.stock),
                    step: 1
                })

                $(row).find("input[name='price']").TouchSpin({
                    verticalbuttons: true,
                    verticalupclass: 'glyphicon glyphicon-plus',
                    verticaldownclass: 'glyphicon glyphicon-minus',
                    min: 0.00,
                    max: 10000000.00,
                    step: 0.01,
                    decimals: 2,
                    prefix: '$',

                })

                $(row).find('input[name="discount"]').TouchSpin({
                    verticalbuttons: true,
                    verticalupclass: 'glyphicon glyphicon-plus',
                    verticaldownclass: 'glyphicon glyphicon-minus',
                    initval: 0.00,
                    min: 0.0,
                    max: 100.0,
                    step: 1.0,
                    decimals: 2,
                    prefix: '%',
                })

            },
            initComplete: function (settings, json) {

            }
        });
    },
};

$(function () {

    select_client = $('#search_client');
    select_search_product = $('#search_product');

    $('.select2').select2({
        language: 'es'
    });

    // Input - Clientes

    select_client.select2({
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: pathname,
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: function (params) {
                return {
                    term: params.term,
                    action: 'search_client'
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: '',
        minimumInputLength: 1,
    })
    .on('select2:select', function (e) {
            var data = e.params.data;
            if (!Number.isInteger(data.id)) {
                return false;
            }
            sale.addClient(data);
        });

    $('.btnAddClient').on('click', function () {
        $('#myModalClient').modal('show');
    });

    $('#myModalClient').on('hidden.bs.modal', function (e) {
        $('#add-client-form').trigger('reset');
    });

    $('#frmClient').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_client');
        submit_with_ajax(pathname, 'Notificación',
            '¿Estas seguro de crear al siguiente cliente?', parameters, function (response) {
                //console.log(response);
                var newOption = new Option(response.full_name, response.id, false, true);
                select_client.append(newOption).trigger('change');
                $('#myModalClient').modal('hide');
            });
    });

    // Input - Productos

    select_search_product.select2({
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: pathname,
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: function (params) {
                return {
                    term: params.term,
                    action: 'search_products',
                    ids: JSON.stringify(sale.getProductsIds())
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese un producto',
        minimumInputLength: 1,
        templateResult: function (repo) {
            if (repo.loading) {
                return repo.text;
            }

            if (!Number.isInteger(repo.id)) {
                return repo.text;
            }

            // var stock = repo.is_active ? repo.stock.stock : 'Sin stock';

            return $(
                '<div class="wrapper container">' +
                '<div class="row">' +
                '<div class="col-lg-1">' +
                '<img alt="" src="' + repo.image + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
                '</div>' +
                '<div class="col-lg-11 text-left shadow-sm">' +
                //'<br>' +
                '<p style="margin-bottom: 0;">' +
                '<b>Nombre:</b> ' + repo.name + '<br>' +
                '</p>' +
                '</div>' +
                '</div>' +
                '</div>');
        },
    })
        .on('select2:select', function (e) {
            var data = e.params.data;
            if (!Number.isInteger(data.id)) {
                return false;
            }
            data.price = 0.00;
            data.quantity = 1;
            data.discount = 0.0;
            data.subtotal = 0.00;
            sale.addProduct(data);
            select_search_product.val('').trigger('change.select2');
        });

    $('#dataSale tbody')
        .off()
        .on('click', 'a[rel="remove"]', function () {
            var tr = dataSale.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
                function () {
                    sale.details.products.splice(tr.row, 1);
                    dataSale.row(tr.row).remove().draw();
                    sale.calculateInvoice();
                }, function () {

                });
        })
        .on('change', 'input[name="price"]', function () {
            console.clear();
            var price = parseFloat($(this).val());
            var tr = dataSale.cell($(this).closest('td, li')).index();
            sale.details.products[tr.row].price = price;
            sale.calculateInvoice();
            $('td:last', dataSale.row(tr.row).node()).html('$' + sale.details.products[tr.row].subtotal.toFixed(2));
        })
        .on('change', 'input[name="quantity"]', function () {
            console.clear();
            var quantity = parseInt($(this).val());
            var tr = dataSale.cell($(this).closest('td, li')).index();
            sale.details.products[tr.row].quantity = quantity;
            sale.calculateInvoice();
            $('td:last', dataSale.row(tr.row).node()).html('$' + sale.details.products[tr.row].subtotal.toFixed(2));
        })
        .on('change', 'input[name="discount"]', function () {
            console.clear();
            var discount = parseFloat($(this).val());
            var tr = dataSale.cell($(this).closest('td, li')).index();
            sale.details.products[tr.row].discount = discount;
            sale.calculateInvoice();
            $('td:last', dataSale.row(tr.row).node()).html('$' + sale.details.products[tr.row].subtotal.toFixed(2));
        });

    // Borrar todos los datos

    $('.btnRemoveAll').on('click', function () {
        if (sale.details.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los details de tu detalle?', function () {
            sale.details.products = [];
            sale.listProducts();
        }, function () {

        });
    });

    // Limpiar la busqueda

    $('.btnClearSearch').on('click', function () {
        select_search_product.val('').focus();
    });

    // Buscar de Modal

    $('.btnSearchProducts').on('click', function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'ids': JSON.stringify(sale.getProductsIds()),
                    'term': select_search_product.val()
                },
                dataSrc: "",
                headers: {
                    'X-CSRFToken': csrftoken
                },
            },
            columns: [
                {"data": "name"},
                {"data": "image"},
                {"data": "stock"},
                {"data": "price"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.is_active) {
                            return '<span class="badge badge-secondary">Sin stock</span>';
                        }
                        return '<span class="badge badge-secondary">' + data + '</span>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a rel="add" class="btn btn-success btn-xs btn-flat"><i class="fas fa-plus"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
        $('#myModalSearchProducts').modal('show');
    });

    $('#tblSearchProducts tbody')
        .off()
        .on('click', 'a[rel="add"]', function () {
            var tr = tblSearchProducts.cell($(this).closest('td, li')).index();
            var product = tblSearchProducts.row(tr.row).data();
            product.quantity = 1;
            product.subtotal = 0.00;
            sale.addProduct(product);
            tblSearchProducts.row($(this).parents('tr')).remove().draw();
        });


    // Envio del formulario de venta

    $('#add-sale-form').on('submit', function (e) {
        e.preventDefault();
        if (sale.details.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }

        var success_url = this.getAttribute('data-url');
        var parameters = new FormData(this);
        parameters.append('products', JSON.stringify(sale.details.products));
        parameters.append('client', JSON.stringify(sale.details.client.id));
        parameters.append('total_discount', JSON.stringify(sale.details.total_discount));
        parameters.append('total_iva', JSON.stringify(sale.details.total_iva));
        parameters.append('total', JSON.stringify(sale.details.total));
        submit_ajax_lot(pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
                    location.href = success_url;
                });

    });
    sale.listProducts();
});

/*
Ver tema Invoice

alert_action('Notificación', '¿Desea imprimir la factura de venta?', function () {
                    window.open('/sales/pdf/' + response.id + '/', '_blank');
                    location.href = success_url;
                }, function () {
                    location.href = success_url;
                });
            });
            */