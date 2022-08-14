from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.exceptions import ObjectDoesNotExist
from .forms import LotForm
from .models import Lot, Stock
from config.permission import ValidatePermission
from .utilities import calculate_stock, get_lot_id, get_total
from django.contrib import messages
# Categories

class AddLot(ValidatePermission, CreateView):
    model = Lot
    form_class = LotForm
    template_name = 'add_lot.html'
    success_url = reverse_lazy('list-stock')
    url_redirect = success_url
    form_error_url = reverse_lazy('add-lot')
    url_render_error = form_error_url
    permission_required = 'add_lot'

    def post(self, request, *args, **kwargs):
        #data
        id_session = request.user.id
        product = request.POST['product']
        quantity = request.POST['quantity']
        price = request.POST['price']
        action = request.POST['action']
        total = get_total(price, quantity, product)
        form = LotForm(request.POST, request.FILES)
        if request.POST == 'add':
            if form.is_valid():
                instance = form.save(commit=False)
                instance.charger_id = id_session
                instance.total = total
                lot_number = get_lot_id()
                try:
                    stock = Stock.objects.get(product_id=product)
                    current_stock =stock.stock
                    stock.stock = calculate_stock(current_stock, quantity)
                    stock.lots.append(lot_number)
                    stock.save()
                    instance.save()
                    messages.success(request, f'El lote N°{lot_number} cargado con éxito')
                    return redirect(self.url_redirect)
                except ObjectDoesNotExist:
                    stock = Stock(
                        product_id=product,
                        stock=quantity,
                        lots=lot_number,
                    )
                    stock.save()
                    instance.save()
                    messages.success(request, f'El lote cargado con éxito, stock inicial producto N°{instance.product.name}')
                    #data = form.save()
                    return redirect(self.url_redirect)
                except Exception as e:
                    print(e)
            else:
                #mensaje de error
                messages.warning(request, f'Hay errores en el formulario, intente nuevamente')
                return redirect(self.url_render_error)

        else:
            return redirect(self.url_redirect)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar lote'
        context['entity'] = 'Lotes'
        context['list_url'] = self.url_redirect
        context['action'] = 'add'
        return context

# List Lot
class ListLot(ValidatePermission, ListView):
    model = Lot
    template_name = 'list_lot.html'
    permission_required = 'view_lot'
    url_redirect = reverse_lazy('list-lot')
    create_url = reverse_lazy('add-lot')

    data = {}
    try:
        lots = Lot.objects.all()

    except Exception as e:
        data['error'] = str(e)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de lotes'
        context['entity'] = 'Lotes'
        context['lots'] = self.lots
        context['list_url'] = self.url_redirect
        context['create_url'] = self.create_url
        return context

# Update Lot
class UpdateLot(ValidatePermission, UpdateView):
    model = Lot
    form_class = LotForm
    template_name = 'add_lot.html'
    success_url = reverse_lazy('list-lot')
    url_redirect = success_url
    permission_required = 'change_lot'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form()
            obj = self.get_object()
            id = obj.id
            if form.is_valid():
                lot = Lot.objects.get(pk=id)
                instance = LotForm(request.POST or None, request.FILES or None, instance=lot)
                product = request.POST['product']
                instance.save()
                messages.success(request, f'Lote editado con éxito, producto: {product}')
                return redirect(self.url_redirect)
            else:
                messages.warning(request, 'Hay errores en el formulario de edición')
                return redirect(self.url_redirect)

# Delete Provider
class DeleteLote(DeleteView, ValidatePermission):
    model = Lot
    success_url = reverse_lazy('list-lot')
    url_redirect = success_url
    permission_required = 'delete_lot'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = self.get_form()
            if form.is_valid():
                lot_id = request.POST['lot_id']
                lot = Lot.objects.get(pk=lot_id)
                lot.delete()
                messages.success(request, f'Lot N°{lot.id}, del producto: {lot.product.name}')
                return redirect(self.url_redirect)
            else:
                messages.warning(request, f'Error al eliminar el lote')
                return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar lot'
        context['entity'] = 'Stock'
        context['list_url'] = self.success_url

        return context


# List Stock
class ListStock(ValidatePermission, ListView):
    model = Lot
    template_name = 'list_stock.html'
    permission_required = 'view_stock'
    url_redirect = reverse_lazy('list-stock')
    create_url = reverse_lazy('add-lot')

    data = {}
    try:
        stocks = Stock.objects.all()

    except Exception as e:
        data['error'] = str(e)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de stock'
        context['entity'] = 'Stock'
        context['stocks'] = Stock.objects.all()
        context['list_url'] = self.url_redirect
        context['create_url'] = self.create_url
        return context